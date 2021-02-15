""" An example of learning a Deep-Q Agent on yaniv
"""
import torch
import os

import rlcard
from rlcard.agents import DQNAgentPytorch as DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed
from rlcard.utils import Logger
from rlcard.games.yaniv.utils import tournament


def main():
    config = {
        "end_after_n_deck_replacements": 0,
        "end_after_n_steps": 100,
        "early_end_reward": -1,
        "seed": 0,
    }

    # Make environment
    env = rlcard.make("yaniv", config=config)
    eval_env = rlcard.make("yaniv", config={**config, "env_num": 2})

    # Set the iterations numbers and how frequently we evaluate/save plot
    evaluate_every = 10
    save_every = 1000
    evaluate_num = 1000
    episode_num = 100000

    # The intial memory size
    memory_init_size = 1000

    # Train the agent every X steps
    train_every = 1

    # The paths for saving the logs and learning curves
    save_dir = "yaniv_dqn"
    log_dir = os.path.join(save_dir, "logs/")
    model_dir = os.path.join(save_dir, "model/")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Set a global seed
    set_global_seed(0)

    agent = DQNAgent(
        scope="dqn",
        action_num=env.action_num,
        replay_memory_init_size=memory_init_size,
        train_every=train_every,
        state_shape=env.state_shape,
        mlp_layers=[512, 512],
        device=torch.device("cpu"),
    )
    random_agent = RandomAgent(action_num=eval_env.action_num)
    env.set_agents([agent, random_agent])
    eval_env.set_agents([agent, random_agent])

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):
        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            payoffs, wins, draws, roundlen = tournament(eval_env, evaluate_num)

            logger.log("\n\n########## Evaluation {} ##########".format(episode))
            logger.log("Timestep: {}, avg roundlen: {}".format(env.timestep, roundlen))
            for i in range(env.player_num):
                logger.log(
                    "Agent {}:\nWins: {}, Draws: {}, Payoff: {}".format(
                        i, wins[i], draws, payoffs[i]
                    )
                )

            logger.log_performance(env.timestep, payoffs[0])

        if episode % save_every == 0:
            torch.save(agent.get_state_dict(), os.path.join(model_dir, "model.pth"))

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot("DQN")

    # Save model
    state_dict = agent.get_state_dict()
    print(state_dict.keys())
    torch.save(state_dict, os.path.join(model_dir, "model.pth"))


if __name__ == "__main__":
    main()
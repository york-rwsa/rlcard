''' A toy example of playing against rule-based bot on UNO
'''

import rlcard
from rlcard import models
from rlcard.agents.yaniv_human_agent import HumanAgent, _print_state, _print_action

# Make environment and enable human mode
# Set 'record_action' to True because we need it to print results
env = rlcard.make('yaniv', config={'record_action': True})
human_agent = HumanAgent()
novice_agent = models.load('yaniv-novice-rule').agents[0]
env.set_agents([human_agent, novice_agent])

print(">> simple yaniv model")

while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action

    final_state = trajectories[0][-1][-2]
    
    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win!')
    else:
        print('You lose!', payoffs[0])
    print('')
    
    break

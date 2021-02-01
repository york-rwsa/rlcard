
import rlcard
from rlcard.utils import set_global_seed
from rlcard.models.yaniv_rule_models import YanivNoviceRuleAgent

# Make environment
env = rlcard.make('yaniv', config={'seed': 0})
episode_num = 2

# Set a global seed
set_global_seed(0)
env.set_agents([
    YanivNoviceRuleAgent(),
    YanivNoviceRuleAgent()
])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))

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
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses ', end='')
        _print_action(pair[1])
        print('')

    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win!')
    else:
        print('You lose!')
    print('')
    
    input("Press any key to continue...")

import gym
import pandas as pd
import matplotlib.pyplot as plt
import time
import blackjack_analysis as black_ai

env = gym.make('Blackjack-v0')
env.seed(0)

def default_policy():
    out = {}
    for i in range(1, 22):
        for j in range(1, 11):
            idx = '(' + str(i) + ', ' + str(j) + ')'
            out[idx] = i < 13
    out['(0, 0)'] = 0
    return out

def get_policy(csv_f):
    out = {}
    df = pd.read_csv(csv_f, index_col = 0)
    for idx in df.index:
        act = df.loc[idx]['Optimal']
        #out[idx] = act
        out[idx] = 1 if act == 'Hit' else 0
    return out
def idx(s):
    return '(' + str(s[0]) + ', '+ str(s[1]) + ')'

# policy = get_policy('optimal_policy.csv')
policy = default_policy()
# print(policy)

state = env.reset()
    
# print(state)

# print(idx(state))
# print(policy[idx(state)])

# print(next_state, payout, done)

num_rounds = 100 *1000
average_payouts = []
win = 0
ai = black_ai.BlackJackAI()
ai.dealer_card(state[1])

nround = 0
while nround < num_rounds:        
    act = policy[idx(state)]
    #act = ai.action(state[0])
    next_state, payout, done, _ = env.step(act)
    # print(next_state, done)
    state = next_state
    if done:
        nround += 1
        state = env.reset()
        ai.dealer_card(state[1])
        if payout > 0:
            win += 1

print("Win Rate: ", 100 * float(win) / (num_rounds),'%')
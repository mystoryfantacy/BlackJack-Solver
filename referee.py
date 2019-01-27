#
import gym
import pandas as pd
import matplotlib.pyplot as plt
import time

import ai_math
import ai_monto_caro

class SimpleAI0():
    def __init__(self):
        self.name = 'Hit-Until-13'
    def action(self, state):
        if state[0] < 13:
            return 1
        return 0

class SimpleAI1():
    def __init__(self):
        self.name = 'Hit-Until-14'
    def action(self, state):
        if state[0] < 14:
            return 1
        return 0

ai_3 = ai_monto_caro.BlackJackAI()
ai_3.LoadPolicy()
agents = [SimpleAI0(), SimpleAI1(), ai_math.BlackJackAI(), ai_3]

def Evaluate(agent, env):
    env.seed(0)
    state = env.reset()

    total_round = 100000
    nround = 0
    win_num = 0
    while nround < total_round:
        next_state, payout, done, _ = env.step(agent.action(state))
        state = next_state
        if done:
            nround += 1
            if payout > 0:
                win_num += 1
            state = env.reset()       
    print("Agent: ", agent.name)
    print("  total games: ", total_round)
    print("  win games: ", win_num)
    print("  win rate: ", float(win_num) / total_round * 100, "%\n")

if __name__ == "__main__":

    env = gym.make('Blackjack-v0')

    for ai in agents:
        Evaluate(ai, env)

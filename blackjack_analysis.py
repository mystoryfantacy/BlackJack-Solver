#
import gym
import pandas as pd
import matplotlib.pyplot as plt
import time

class BlackJackAI():
    def __init__(self):
        self.prob = [[0 for i in range(0,23)] for i in range(0, 23)]
        self.card_prob = [ 1 for i in range(11) ]
        self.card_prob[10] = 4

        for x in range(1, 11):
            self.prob[1][x] = self.card_prob[x]
        
        for n in range(2, 22):
            for y in range(1, 22):
                for z in range(1, 11):
                    v = y + z
                    if v > 21:
                        v = 22
                    self.prob[n][v] += self.prob[n-1][y] * self.card_prob[z]
        
        self.count = [0] * 31
        for i in range(1, 22):
            for j in range(1, i+1):
                self.count[i] += self.prob[j][i]
        
        self.prob_percent = [[0 for i in range(0,23)] for i in range(0, 23)] 
        for n in range(1, 22):
            tmp = 0
            for x in range(1, 23):
                tmp += self.prob[n][x]
            for x in range(1, 23):
                self.prob_percent[n][x] = self.prob[n][x] / float(tmp)

    def dealer_card(self, a):
        final_prob = [0] * 31
        for i in range(17, 31):
            final_prob[i] = self.count[i - a]
            if final_prob[i] == 0:
                continue
            for j in range(i-1, 16, -1):
                final_prob[i] -= self.count[j - a]
    
        t = 0
        for i in final_prob[17:]:
            t += i
        
        self.dealer_prob = [0] * 31
        for i in range(17, 22):
            self.dealer_prob[i] = float(final_prob[i]) / t
    
        self.bust = 0
        for i in range(22, 31):
            self.bust += final_prob[i]
        self.bust = self.bust / float(t)
 

    def stand_win(self, n):
        win_rate = self.bust
        for i in range(17, n):
            win_rate += self.dealer_prob[i]
        return win_rate
    
    def hit_win_step(self, n, step):
        win_rate = 0
        for i in range(n+1, 22):
            win_rate += self.prob_percent[step][i - n] * self.stand_win(i)
        return win_rate

    def hit_win(self, n):
        win_rate = 0.0
        for i in range(1, 22 - n):
            win_rate = max(win_rate,self.hit_win_step(n, i))
        return win_rate

    def action(self, n):
        # print(n)
        return n < 12
        if self.stand_win(n) < self.hit_win(n):
            return 1
        else:
            return 0

if __name__ == "__main__":
    ai = BlackJackAI()
    
    ai.dealer_card(8)
    print("11 stand", ai.stand_win(11))
    print("11 hit", ai.hit_win(11))

    env = gym.make('Blackjack-v0')
    env.seed(1)
    state = env.reset()
    ai.dealer_card(state[1])

    total_round = 100000
    nround = 0
    win_num = 0
    while nround < total_round:
        next_state, payout, done, _ = env.step(ai.action(state[0]))
        state = next_state
        if done:
            nround += 1
            if payout > 0:
                win_num += 1
            state = env.reset()
            ai.dealer_card(state[1])        

    print("total games: ", total_round)
    print("win games: ", win_num)
    print("win rate: ", float(win_num) / total_round * 100, "%")
#

import gym
import numpy as np

show_step = 1000

def _str(s, a = None):
    i, j, k = s
    if k:
        k = 1
    else:
        k = 0
    s = str(i) + '_' + str(j) + '_' + str(k)
    if a:
        s += '_' + str(a)
    return s

class BlackJackAI(object):
    """docstring for BlackJackAI"""
    def __init__(self):
        super(BlackJackAI, self).__init__()
        self.name = 'MontoCaro-AI'
        self.state_act_pair = {}
        self.policy = {}


    def _ResetTable(self):
        self.state_act_pair = {}
        for i in range(1, 22):
            for j in range(1, 12):
                self.state_act_pair[_str((i, j, 1), 0)] = [0, 0]
                self.state_act_pair[_str((i, j, 1), 1)] = [0, 0]
                self.state_act_pair[_str((i, j, 0), 0)] = [0, 0]
                self.state_act_pair[_str((i, j, 0), 1)] = [0, 0]

    def GetAction(self, state):
        return np.random.randint(0, 2)

    def Learn(self):
        self._ResetTable()
        env = gym.make('Blackjack-v0')
        env.seed(0)

        state = env.reset()
        nround = 0
        total_round = 5000000
        track = []
        while nround < total_round:
            act = self.GetAction(state)
            track.append(_str(state, act))
            next_state, payout, done, _ = env.step(act)
            state = next_state
            if done:
                if payout > 0:
                    for p in track:
                        self.state_act_pair[p][0] += 1
                for p in track:
                    self.state_act_pair[p][1] += 1
                nround += 1
                if nround % show_step == 0:
                    print(nround, total_round, nround/float(total_round)*100, '%')
                state = env.reset()
                if nround % 5000 == 0:
                    env.seed(np.random.randint(0,11))
                track = []
        self._MakePolicy()
    
    def _StateActPairStr(self, state):
        def view_res(state, act):
            s = _str(state, act)
            w0 = self.state_act_pair[s][0]
            t0 = self.state_act_pair[s][1]
            return str(w0)+ '/'+ str(t0) + '['+str(w0/(float(t0)+0.0001)) + ']'
        return view_res(state, 0) + ' '  + view_res(state, 1) 

    def _MakePolicy(self):
        def _rate(i, j, k, a):
            s = _str((i, j, k), a)
            p = float(self.state_act_pair[s][0]) / (float(self.state_act_pair[s][0]) + 0.0001)
            return p

        def _act(i, j, k):
            p0 = _rate(i, j, k, 0)
            p1 = _rate(i, j, k, 1)
            if p0 < p1:
                return 1
            else:
                return 0

        self.policy = {}
        for i in range(1, 22):
            for j in range(1, 12):
                for k in range(0, 2):
                    self.policy[_str((i, j, k))] = (_act(i, j, k), (i, j, k))
        
    def SavePolicy(self):
        with open('BlackJackPolicy.txt', 'w') as f:
            for s,a in self.policy.items():
                f.write(s + ' ' + str(a[0]) + ' ' + self._StateActPairStr(a[1]) + '\n')
    
    def LoadPolicy(self):
        self.policy = {}
        with open('BlackJackPolicy.txt', 'r') as f:
            for l in f.readlines():
                ws = l.strip().split()
                s,a = ws[0:2]
                self.policy[s] = int(a)

    def PrintPolicy(self):
        print(self.policy)  

    def action(self, state):
        a = self.policy[_str(state)]
        return a

if __name__ == '__main__':
    ai = BlackJackAI()
    ai.Learn()
    ai.SavePolicy()
    ai.PrintPolicy()
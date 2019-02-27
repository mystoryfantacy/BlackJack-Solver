#

import gym
import math
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras import losses
from generate_dataset import *

model = Sequential()
model.add(Dense(16, input_shape=(3,)))
model.add(Activation('relu'))
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dense(2))
model.add(Activation('softmax'))

model.compile(optimizer='rmsprop',
              loss='mean_squared_error',
              metrics=[losses.mean_squared_error])

early_stop_callback = keras.callbacks.EarlyStopping(monitor='mean_squared_error', min_delta=1e-5, patience=100, verbose=0, mode='min', baseline=None, restore_best_weights=False)

show_step = 1000

def _hash(s, a = None):
    i, j, k = s
    if k:
        k = 1
    else:
        k = 0
    if not a == None:
        return (i, j, k, a)
    else:
        return (i, j, k)

class BlackJackAI(object):
    """docstring for BlackJackAI"""
    def __init__(self):
        super(BlackJackAI, self).__init__()
        self.name = 'MontoCaro-AI'
        self.state_act_pair = {}
        self.state_visit_cnt = {}
        self.policy = {}
        self.factor = 0.05

    def SetUBC(self):
        self.sample_by_ubc = True

    def ResetUBC(self):
        self.sample_by_ubc = False

    def _ResetTable(self):
        self.state_act_pair = {}
        for i in range(1, 22):
            for j in range(1, 12):
                self.state_visit_cnt[(i, j, 1)] = 0
                self.state_visit_cnt[(i, j, 0)] = 0
                self.state_act_pair[(i, j, 1, 0)] = [0, 0, 1.0]
                self.state_act_pair[(i, j, 1, 1)] = [0, 0, 1.0]
                self.state_act_pair[(i, j, 0, 0)] = [0, 0, 1.0]
                self.state_act_pair[(i, j, 0, 1)] = [0, 0, 1.0]

    def _UBC(self, state, act):
        N_s = self.state_visit_cnt[_hash(state)]
        N_s_a, Q_s_a = self.state_act_pair[_hash(state, act)][1:3]
        ubc = Q_s_a + \
              math.sqrt(math.log(1+N_s) / (1 + N_s_a))
        return ubc

    def _GetAction(self, state):
        if self.sample_by_ubc:
          if self._UBC(state, 1) > self._UBC(state, 0):
              return 1
          else:
              return 0
        else:
          N_s = self.state_visit_cnt[_hash(state)]
          N_0, Q_0 = self.state_act_pair[_hash(state, 0)][1:3]
          N_1, Q_1 = self.state_act_pair[_hash(state, 1)][1:3]
          log_Q0 = math.log(N_0 + 1) * Q_0
          log_Q1 = math.log(N_1 + 1) * Q_1
          delta_p = (log_Q0 - log_Q1) / float(log_Q0 + log_Q1 + 1e-5) * 1e-3
          prob = self.policy[state]
          prob[0] = min(max(0, prob[0] + delta_p), 1)
          prob[1] = min(max(0, prob[1] - delta_p), 1)
          ubc0 = prob[0] * \
                 math.sqrt(math.log(1+N_s) / (1 + N_0))
          ubc1 = prob[1] * \
                 math.sqrt(math.log(1+N_s) / (1 + N_1))
          return 0 if ubc0 >= ubc1 else 1
          #act = np.random.choice(a=2, size=1, replace=True, p=prob)[0]
          #return act


    def _MonteCarlo(self):
        self._ResetTable()
        env = gym.make('Blackjack-v0')
        env.seed(0)

        state = env.reset()
        nround = 0
        total_round = 50000
        track = []
        while nround < total_round:
            act = self._GetAction(state)
            track.append(_hash(state, act))
            next_state, payout, done, _ = env.step(act)
            state = next_state
            if done:
                # print('track_len', len(track))
                # print('track', track)
                if payout > 0:
                    for p in track:
                        self.state_act_pair[p][0] += 1
                for p in track:
                    self.state_act_pair[p][1] += 1
                    self.state_act_pair[p][2] =  \
                        float(self.state_act_pair[p][0]) \
                        / float(self.state_act_pair[p][1])
                    self.state_visit_cnt[(p[0], p[1], p[2])] += 1
                nround += 1
                if nround % show_step == 0:
                    print(nround, total_round, nround/float(total_round)*100, '%')
                state = env.reset()
                if nround % 5000 == 0:
                    env.seed(np.random.randint(0,11))
                track = []

    def _CollectData(self):
        sample_threshold = 100

        data = []
        label = []
        def _subroutine(i, j, k):
            if self.state_visit_cnt[(i, j, k)] >= sample_threshold:
                data.append([i,j,k])
                n_act_sum = self.state_act_pair[(i, j, k, 0)][1] \
                            + self.state_act_pair[(i, j, k, 1)][1]
                p0 = self.state_act_pair[(i, j, k, 0)][1] / float(n_act_sum)
                p1 = self.state_act_pair[(i, j, k, 1)][1] / float(n_act_sum)
                label.append([p0, p1])

        for i in range(1, 22):
            for j in range(1, 12):
                _subroutine(i, j, 0)
                _subroutine(i, j, 1)
        self.data = np.array(data)
        self.label = np.array(label)
        print('data:',self.data[0:10])
        print('label:',self.label[0:10])

    def Train(self, epochs = 100):
        for i in range(epochs):
            self._ResetTable()
            self._MakePolicy()
            self._MonteCarlo()
            self._CollectData()
            print('Training Data Size: ', len(self.data))
            model.fit(self.data, self.label, epochs=100, batch_size=32, callbacks=[early_stop_callback])
        self._MakePolicy()
        self.PrintPolicy()

    def _StateActPairStr(self, state):
        def view_res(state, act):
            s = _str(state, act)
            w0 = self.state_act_pair[s][0]
            t0 = self.state_act_pair[s][1]
            return str(w0)+ '/'+ str(t0) + '['+str(w0/(float(t0)+0.0001)) + ']'
        return view_res(state, 0) + ' '  + view_res(state, 1)

    def _MakePolicy(self):
        self.policy = {}
        for i in range(1, 22):
            for j in range(1, 12):
                _state = np.array([[i, j, 0]])
                act_prob = model.predict(_state)
                self.policy[(i,j,0)] = act_prob[0]
                _state = np.array([[i, j, 1]])
                act_prob = model.predict(_state)
                self.policy[(i,j,1)] = act_prob[0]

    def SavePolicy(self):
        model.save('BlackJack_MC_DQN_v0.h5')

    def LoadPolicy(self):
        model.load('BlackJack_MC_DQN_v0.h5')
        self._MakePolicy()

    def PrintPolicy(self):
        for k,d in self.policy.items():
            print(k, d)

    def action(self, state):
        act = np.random.choice(a=2, size=1, replace=False, p=self.policy[state])
        return act[0]

if __name__ == '__main__':
    ai = BlackJackAI()
    ai.SetUBC()
    ai.Train(10)
    input("Ending Warmup. Please input any key to continue")
    ai.ResetUBC()
    for i in range(3):
        ai.Train(10)
        print("End of iter ", i)
        input("Please input any key to continue")
    ai.SavePolicy()

import keras
from keras.models import load_model
import numpy as np


class BlackJackAI():
    def __init__(self, model_name = './DQN/BlackJack_keras_v0.h5', sample_action = False):
        self.name = 'AI_DQN [' + model_name + ']'
        self.model = load_model(model_name)
        self._GetPolicy()
        self.sample_action = sample_action

    def _GetPolicy(self):
        self.policy = {}
        for i in range(1, 22):
            for j in range(1, 12):
                _state = np.array([[i, j, 0]])
                act_prob = self.model.predict(_state)
                self.policy[(i,j,0)] = act_prob[0]
                _state = np.array([[i, j, 1]])
                act_prob = self.model.predict(_state)
                self.policy[(i,j,1)] = act_prob[0]


    def action(self, state):
        if self.sample_action:
            act = np.random.choice(a=2, size=1, replace=False, p=self.policy[state])
            return act[0]
        else:
            return np.argmax(self.policy[state])

if __name__ == '__main__':
    ai = BlackJackAI()
    print(ai.action((0, 0, 0)))

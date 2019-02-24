import keras
from keras.models import load_model
import numpy as np


class BlackJackAI():
    def __init__(self, model_name = './DQN/BlackJack_keras_v0.h5'):
        self.name = 'AI_DQN'
        self.model = load_model(model_name)
        self._GetPolicy()

    def _GetPolicy(self):
        self.policy = {}
        for i in range(1, 22):
            for j in range(1, 12):
                _state = np.array([[i, j, 0]])
                act = self.model.predict(_state)
                self.policy[(i,j,0)] = np.argmax(act)
                _state = np.array([[i, j, 1]])
                act = self.model.predict(_state)
                self.policy[(i,j,1)] = np.argmax(act)


    def action(self, state):
        return self.policy[(state[0], state[1], state[2])]

if __name__ == '__main__':
    ai = BlackJackAI()
    print(ai.action((0, 0, 0)))

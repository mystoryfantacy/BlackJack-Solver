import keras
from keras.models import load_model
import numpy as np


class BlackJackAI():
    def __init__(self, model_name = './DQN/BlackJack_keras.h5'):
        self.name = 'AI_DQN'
        self.model = load_model(model_name)

    def action(self, state):
        _state = np.array([[state[0], state[1], state[2]]])
        act = self.model.predict(_state)
        return np.argmax(act)

if __name__ == '__main__':
    ai = BlackJackAI()
    print(ai.action((0, 0, 0)))

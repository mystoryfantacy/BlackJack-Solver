#!

import os

class Units:
    def __init__(self):
        self.state = (0, 0, 0)
        self.action = 0
        self.hit_num = 0
        self.hit_win_num = 0
        self.stand_num = 0
        self.stand_win_num = 0

    def __str__(self):
        s = str(self.state) + ' ' + str(self.action) + ' ' + str(self.hit_num)
        s += ' ' + str(self.hit_win_num) + ' ' + str(self.stand_num)
        s += ' ' + str(self.stand_win_num)
        return s

samples = []
with open('../BlackJackPolicy.txt', 'r') as f:
    for l in f.readlines():
        sample = Units();
        ds = l.strip().split()
        (a, b, c) = ds[0].split('_')
        sample.state = (int(a), int(b), int(c))
        sample.action = int(ds[1])
        (a, b) = ds[2].split('[')[0].split('/')
        sample.stand_num = int(a)
        sample.stand_win_num = int(b)
        (a, b) = ds[3].split('[')[0].split('/')
        sample.hit_num = int(a)
        sample.hit_win_num = int(b)
        samples.append(sample)

print(len(samples))
for s in samples[0:10]:
  print(s)


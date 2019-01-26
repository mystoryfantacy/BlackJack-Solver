class BlackJackAI():
    def __init__(self):
        self.dealer_card = -1
        self.name = 'AI_MATH'
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

    def update_dealer_card(self, a):
        if a == self.dealer_card:
            return
        self.dealer_card = a
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

    def action(self, state):
        self.update_dealer_card(state[1])
        n = state[0]
        hit_win_rate = self.hit_win(n)
        if state[2]:
            hit_win_rate = max(hit_win_rate, self.hit_win(n - 10))
        if self.stand_win(n) < hit_win_rate:
            return 1
        else:
            return 0
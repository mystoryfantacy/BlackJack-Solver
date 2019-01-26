#

prob = [[0 for i in range(0,23)] for i in range(0, 23)]

card_prob = [1.0 / 13.0] * 12

card_prob[10] = 4.0 / 13.0
card_prob = [ 1 for i in range(11) ]
card_prob[10] = 4
print('card_prob', card_prob)

for x in range(1, 11):
    prob[1][x] = card_prob[x]

for n in range(2, 22):
    for y in range(1, 22):
        for z in range(1, 11):
            v = y + z
            if v > 21:
                v = 22
            prob[n][v] += prob[n-1][y] * card_prob[z]

print(prob[:][22])
for n in range(1,22):
  print(prob[n][22])

total_prob = [0 for i in range(23)]
for n in range(1, 22):
    for x in range(1, 23):
        total_prob[x] += prob[n][x]
        if x == 22:
            print(total_prob[x], prob[n][x])

# print(total_prob)
total = 0
for x in range(1, 23):
    total += total_prob[x]

for x in range(1, 23):
    print(x, total_prob[x] / float(total))

print(prob[1][2], prob[2][2])
count = [0] * 28
for i in range(1, 22):
    for j in range(1, i+1):
        count[i] += prob[j][i]
print("count: ", count)

prob_percent = [[0 for i in range(0,23)] for i in range(0, 23)] 
for n in range(1, 22):
    tmp = 0
    for x in range(1, 23):
        tmp += prob[n][x]
    for x in range(1, 23):
        prob_percent[n][x] = prob[n][x] / float(tmp)



def dealer_prob(a):
    final_prob = [0] * 28
    for i in range(17, 28):
        final_prob[i] = count[i - a]
        if final_prob[i] == 0:
            continue
        for j in range(i-1, 16, -1):
            final_prob[i] -= count[j - a]
    return final_prob

a = 5
final_prob = dealer_prob(a)
print(final_prob[17:])

t = 0
for i in final_prob[17:]:
    t += i

for i in range(17, 22):
    final_prob[i] = float(final_prob[i]) / t
    print(i, final_prob[i])
bust = 0
for i in range(22, 28):
    bust += final_prob[i]
bust = bust/float(t)
print('bust', bust)
# print(final_prob[17:])

def stand_win(n):
    win_rate = bust
    for i in range(17, n):
        win_rate += final_prob[i]
    return win_rate

print("16 stand", stand_win(16))
print("17 stand", stand_win(17))
print("20 stand", stand_win(20))

def hit_win_step(n, step):
    win_rate = 0
    for i in range(n+1, 22):
        win_rate += prob_percent[step][i - n] * stand_win(i)
    return win_rate

def hit_win(n):
    win_rate = 0.0
    for i in range(1, 22 - n):
        win_rate = max(win_rate, hit_win_step(n, i))
    return win_rate

print("16 hit1", hit_win_step(16, 1))
print("16 hit2", hit_win_step(16, 2))
print("16 hit3", hit_win_step(16, 3))
print("16 hit", hit_win(16))

print("17 hit1", hit_win_step(17, 1))
print("17 hit2", hit_win_step(17, 2))
print("17 hit3", hit_win_step(17, 3))
print("17 hit", hit_win(17))

print("20 hit1", hit_win_step(20, 1))
print("20 hit2", hit_win_step(20, 2))
print("20 hit3", hit_win_step(20, 3))
print("20 hit", hit_win(20))
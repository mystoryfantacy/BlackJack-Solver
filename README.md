# BlackJack-Solver
BlackJack-Solver Collection tries to collect different Algorithm to play BlackJack well.

`Target` Win Game BlackJack    [Kaggle Example](https://www.kaggle.com/learn-forum/58735#latest-348767])

What can be tried? Random Action, Evaluate Action with Monto Carlo, Predict Next State and Reward with DNN.

1. Two empirical algorithms

2. An analytic algorithm

3. Monte-Carlo algorithm

4. DQN algorithm

And the performance results are as below:

```
Agent:  Hit-Until-13
  total games:  100000
  win games:  42462
  win rate:  42.462 %

Agent:  Hit-Until-14
  total games:  100000
  win games:  41784
  win rate:  41.784 %

Agent:  AI_MATH
  total games:  100000
  win games:  41549
  win rate:  41.549 %

Agent:  MontoCaro-AI
  total games:  100000
  win games:  42916
  win rate:  42.916 %

Agent:  AI_DQN [./DQN/BlackJack_keras_v0.h5]
  total games:  100000
  win games:  42843
  win rate:  42.842999999999996 %

Agent:  AI_DQN [./DQN/BlackJack_MC_DQN_v0.h5]
  total games:  100000
  win games:  42233
  win rate:  42.233 %

```

Because of the simplicity of BlackJack and the small state space, Monte-Carlo method can get the best performance
in this game. A DNN trained with data sampled in Monte-Carlo algorithm can get the second best performance. And a simple
empirical algorithm does well unexpectedly. It's possible to traverse all states exhaustedly and the analytic algorithm
 indeed did in this way. However the performance is a little upset maybe due to I mistook something. I also tried an algorithm
 combining Monte-Carlo and DNN training, it could get a not bad performance but couldn't compete with DNN directily trained
 with data from a pure Monte-Carlo. I think it's because the pure Monte-Carlo can collect all state and state-action values
 thanks to the small state space, but comination algorithm always missed some states.  

 Finally, it still needs more efforts to explain everything clearly but at least it shows how DNN and Monte-Carlo can be used
 to solve optimization problems.

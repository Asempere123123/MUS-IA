from gymnasium import Env
from gymnasium.spaces import Discrete, Box
from random import shuffle
from utils import *

from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv

class musEnv(Env):
    def __init__(self):
        #Cantidad acciones
        self.action_space = Discrete(16)

        #todas las opciones
        #card_space = tuple((Discrete(10),))  # Discrete(10) for ranks (1 to 12)
        self.observation_space = Box(low=1, high=10, shape=(4,), dtype=int)#tuple((card_space, card_space, card_space, card_space))

        #set starting hand and deck
        self.deck = BARAJA_ESPAÑOLA.copy()
        shuffle(self.deck)

        hand = []
        hand.append(self.deck[-1])
        self.deck.pop()
        hand.append(self.deck[-1])
        self.deck.pop()
        hand.append(self.deck[-1])
        self.deck.pop()
        hand.append(self.deck[-1])
        self.deck.pop()

        self.state = hand

    def step(self, action):

        #Calculate initial hand score
        p = Player(self.state, [0, 0, 0, 0])
        get_hand_scores(p)

        iScore = sum(p.score)

        # Convert the integer to a set of 4 booleans
        bit_mask = 1
        newAction = []

        for _ in range(4):
            newAction.append(action & bit_mask != 0)
            bit_mask <<= 1

        #Aply action
        for i in range(4):
            if newAction[i]:
                self.state[i] = self.deck[-1]
                self.deck.pop()

        #Calculate final and delta hand score
        p = Player(self.state, [0, 0, 0, 0])
        get_hand_scores(p)

        fScore = sum(p.score)

        dScore = fScore - iScore

        reward = dScore #igual -1, hay qque experimentar

        done = True

        info = {}

        return self.state, reward, done, False, info

    def render(self):
        pass

    def reset(self, seed=None, options=None):

        super().reset(seed=seed)

        self.deck = BARAJA_ESPAÑOLA.copy()
        shuffle(self.deck)

        hand = []
        hand.append(self.deck[-1])
        self.deck.pop()
        hand.append(self.deck[-1])
        self.deck.pop()
        hand.append(self.deck[-1])
        self.deck.pop()
        hand.append(self.deck[-1])
        self.deck.pop()

        self.state = hand

        return self.state, {}

    
env = musEnv()


"""
# Instantiate the agent
#model = DQN("MlpPolicy", env, verbose=1)
model = DQN.load("dqn_mus30m", env=env)
# Train the agent and display a progress bar
model.learn(total_timesteps=int(2e7), progress_bar=True)
# Save the agent
model.save("dqn_mus30m")"""


# Load the trained agent
# NOTE: if you have loading issue, you can pass `print_system_info=True`
# to compare the system on which the model was trained vs the current one
# model = DQN.load("dqn_mus", env=env, print_system_info=True)
model = DQN.load("dqn_mus30m", env=env)

"""
# Evaluate the agent
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=1000000)
print(mean_reward, std_reward)"""

#predecir
i = ""
while(i == ""):
    #PREDECIR MANO ALEATORIA
    deck = BARAJA_ESPAÑOLA.copy()
    shuffle(deck)

    hand = []
    hand.append(deck[-1])
    deck.pop()
    hand.append(deck[-1])
    deck.pop()
    hand.append(deck[-1])
    deck.pop()
    hand.append(deck[-1])
    deck.pop()

    action, _states = model.predict(hand, deterministic=True)

    # Convert the integer to a set of 4 booleans
    bit_mask = 1
    newAction = []

    for _ in range(4):
        newAction.append(action & bit_mask != 0)
        bit_mask <<= 1

    #Calculate initial hand score
    p = Player(hand, [0, 0, 0, 0])
    get_hand_scores(p)

    iScore = sum(p.score)

    print(hand)
    print(newAction)

    #Aply action
    for i in range(4):
        if newAction[i]:
            hand[i] = deck[-1]
            deck.pop()

    print(hand)

    #Calculate final and delta hand score
    p = Player(hand, [0, 0, 0, 0])
    get_hand_scores(p)

    fScore = sum(p.score)

    dScore = fScore - iScore
    print(dScore)

    i = input()
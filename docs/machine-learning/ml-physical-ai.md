---
title: Machine Learning for Physical AI
sidebar_position: 6
description: Reinforcement learning, imitation learning, and embodied AI algorithms
---

# Machine Learning for Physical AI

Machine learning in physical AI systems differs fundamentally from traditional ML applications due to the embodied nature of the learning agent. Physical AI systems must learn through interaction with the real world, dealing with continuous state and action spaces, partial observability, and the high cost of failed actions.

Reinforcement learning (RL) is particularly well-suited for physical AI applications, as it frames learning as a sequential decision-making problem where an agent learns to maximize cumulative reward through environmental interaction. In robotics, the reward function can encode task completion, energy efficiency, safety constraints, or other performance metrics. Deep reinforcement learning extends these concepts by using neural networks to represent policies and value functions, enabling complex behaviors in high-dimensional state spaces.

Imitation learning allows robots to acquire skills by observing and replicating human demonstrations. This approach can significantly reduce the sample complexity compared to pure reinforcement learning, as the robot learns from expert demonstrations rather than through trial and error. Behavioral cloning, inverse reinforcement learning, and generative adversarial imitation learning (GAIL) are common approaches in this domain.

The reality gap represents one of the key challenges in physical AI learning: models trained in simulation often fail to transfer to the real world due to discrepancies between simulated and real physics, sensor noise, and unmodeled dynamics. Domain randomization, domain adaptation, and system identification techniques help bridge this gap by making learned policies more robust to environmental variations.

Transfer learning enables knowledge gained in one context to be applied to related tasks, reducing the amount of experience needed to learn new skills. This is particularly important for physical AI systems where real-world experience is expensive and potentially risky.

```python
import torch
import torch.nn as nn
import numpy as np
from collections import deque
import random

class ActorNetwork(nn.Module):
    """Actor network for continuous action space"""
    def __init__(self, state_dim, action_dim, max_action):
        super(ActorNetwork, self).__init__()

        self.l1 = nn.Linear(state_dim, 256)
        self.l2 = nn.Linear(256, 256)
        self.l3 = nn.Linear(256, action_dim)

        self.max_action = max_action

    def forward(self, state):
        a = torch.relu(self.l1(state))
        a = torch.relu(self.l2(a))
        action = torch.tanh(self.l3(a)) * self.max_action
        return action

class CriticNetwork(nn.Module):
    """Critic network for action-value estimation"""
    def __init__(self, state_dim, action_dim):
        super(CriticNetwork, self).__init__()

        self.l1 = nn.Linear(state_dim + action_dim, 256)
        self.l2 = nn.Linear(256, 256)
        self.l3 = nn.Linear(256, 1)

    def forward(self, state, action):
        sa = torch.cat([state, action], 1)
        q = torch.relu(self.l1(sa))
        q = torch.relu(self.l2(q))
        q = self.l3(q)
        return q

class DDPGAgent:
    """Deep Deterministic Policy Gradient agent for continuous control"""
    def __init__(self, state_dim, action_dim, max_action, lr_actor=1e-4, lr_critic=1e-3):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.actor = ActorNetwork(state_dim, action_dim, max_action).to(self.device)
        self.actor_target = ActorNetwork(state_dim, action_dim, max_action).to(self.device)
        self.actor_target.load_state_dict(self.actor.state_dict())

        self.critic = CriticNetwork(state_dim, action_dim).to(self.device)
        self.critic_target = CriticNetwork(state_dim, action_dim).to(self.device)
        self.critic_target.load_state_dict(self.critic.state_dict())

        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=lr_actor)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=lr_critic)

        self.replay_buffer = deque(maxlen=1000000)
        self.batch_size = 100
        self.gamma = 0.99  # Discount factor
        self.tau = 0.005   # Target network update rate

    def select_action(self, state, add_noise=True, noise_scale=0.1):
        state = torch.FloatTensor(state.reshape(1, -1)).to(self.device)
        action = self.actor(state).cpu().data.numpy().flatten()

        if add_noise:
            noise = np.random.normal(0, noise_scale, size=action.shape)
            action = action + noise
            action = np.clip(action, -1, 1)  # Assuming normalized action space

        return action

    def store_transition(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        # Sample batch from replay buffer
        batch = random.sample(self.replay_buffer, self.batch_size)
        state, action, reward, next_state, done = map(np.stack, zip(*batch))

        state = torch.FloatTensor(state).to(self.device)
        action = torch.FloatTensor(action).to(self.device)
        reward = torch.FloatTensor(reward).to(self.device).unsqueeze(1)
        next_state = torch.FloatTensor(next_state).to(self.device)
        done = torch.BoolTensor(done).to(self.device).unsqueeze(1)

        # Compute target Q-value
        next_action = self.actor_target(next_state)
        target_Q = self.critic_target(next_state, next_action)
        target_Q = reward + (self.gamma * target_Q * (1 - done))

        # Critic update
        current_Q = self.critic(state, action)
        critic_loss = nn.MSELoss()(current_Q, target_Q.detach())

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Actor update
        actor_loss = -self.critic(state, self.actor(state)).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Update target networks
        for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)

        for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
            target_param.data.copy_(self.tau * param.data + (1 - self.tau) * target_param.data)
``

When implementing reinforcement learning for physical robots, always start with safety constraints and consider using constrained RL methods that guarantee safety during learning. Implement multiple layers of safety checks including joint limits, velocity limits, and force limits.



![ML for Physical AI](./assets/ml-physical-ai.png)

The integration of machine learning with physical systems enables robots to adapt and improve their performance through experience, making them more capable and robust in real-world applications.
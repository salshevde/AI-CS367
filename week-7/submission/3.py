import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

class EpsilonGreedyBinaryBandit:
    def __init__(self, epsilon: float = 0.1):
        """
        Initialize epsilon-greedy binary bandit.
        
        Args:
            epsilon (float): Exploration rate (default: 0.1)
        """
        self.epsilon = epsilon
        self.num_arms = 2
        self.Q = np.zeros(self.num_arms)  # Value estimates
        self.N = np.zeros(self.num_arms)  # Action counts
        
    def select_action(self) -> int:
        """
        Select action using epsilon-greedy strategy.
        
        Returns:
            int: Selected action (0 or 1)
        """
        if np.random.random() < self.epsilon:
            # Explore: choose random action
            return np.random.randint(self.num_arms)
        else:
            # Exploit: choose best action (random tie-breaking)
            return np.random.choice(np.where(self.Q == self.Q.max())[0])
    
    def update(self, action: int, reward: float):
        """
        Update value estimates and counts.
        
        Args:
            action (int): Selected action
            reward (float): Received reward
        """
        self.N[action] += 1
        self.Q[action] += (1.0 / self.N[action]) * (reward - self.Q[action])

def run_binary_bandit(num_iterations: int) -> Tuple[float, List[int], List[float]]:
    """
    Run the binary bandit experiment.
    
    Args:
        num_iterations (int): Number of iterations to run
        
    Returns:
        Tuple containing:
        - total_reward (float)
        - action_counts (list)
        - rewards (list)
    """
    bandit = EpsilonGreedyBinaryBandit()
    total_reward = 0
    rewards = []
    
    for _ in range(num_iterations):
        action = bandit.select_action()
        
        # This should be replaced with actual bandit call
        # reward = binary_bandit_a(action) or binary_bandit_b(action)
        reward = np.random.binomial(1, 0.5)  # Placeholder
        
        bandit.update(action, reward)
        total_reward += reward
        rewards.append(reward)
    
    return total_reward, bandit.N.tolist(), rewards

class NonStationaryBandit:
    def __init__(self, n_arms: int = 10):
        """
        Initialize non-stationary bandit.
        
        Args:
            n_arms (int): Number of arms (default: 10)
        """
        self.n_arms = n_arms
        self.q_values = np.zeros(n_arms)
        
    def get_reward(self, action: int) -> float:
        """
        Get reward for selected action.
        
        Args:
            action (int): Selected action (0-9)
            
        Returns:
            float: Reward value
        """
        # Random walk step for all arms
        self.q_values += np.random.normal(0, 0.01, self.n_arms)
        
        # Return reward with noise
        true_value = self.q_values[action]
        return np.random.normal(true_value, 1.0)

def test_nonstationary_bandit(num_iterations: int):
    """
    Test the non-stationary bandit and visualize results.
    
    Args:
        num_iterations (int): Number of iterations to run
    """
    bandit = NonStationaryBandit()
    rewards = []
    q_values_history = []
    
    for _ in range(num_iterations):
        action = np.random.randint(10)  # Random action selection
        reward = bandit.get_reward(action)
        rewards.append(reward)
        q_values_history.append(bandit.q_values.copy())
    
    # Plot rewards
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(rewards)
    plt.xlabel('Time step')
    plt.ylabel('Reward')
    plt.title('Rewards Over Time')
    
    # Plot Q-values evolution
    plt.subplot(1, 2, 2)
    q_values_history = np.array(q_values_history)
    for arm in range(10):
        plt.plot(q_values_history[:, arm], label=f'Arm {arm}')
    plt.xlabel('Time step')
    plt.ylabel('True value')
    plt.title('True Values Evolution')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Test binary bandit
    num_iterations = 1000
    total_reward, action_counts, rewards = run_binary_bandit(num_iterations)
    print(f"Total reward: {total_reward}")
    print(f"Action counts: {action_counts}")
    print(f"Average reward: {total_reward / num_iterations:.3f}")
    
    # Test non-stationary bandit
    test_nonstationary_bandit(1000)
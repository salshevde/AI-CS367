import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class NonStationaryBandit:
    def __init__(self, n_arms: int = 10):
        self.n_arms = n_arms
        self.q_values = np.zeros(n_arms)
        
    def get_reward(self, action: int) -> float:
        # Random walk for all arms
        self.q_values += np.random.normal(0, 0.01, self.n_arms)
        
        # Return reward with noise
        true_value = self.q_values[action]
        return np.random.normal(true_value, 1.0)

class RecencyWeightedEpsilonGreedy:
    def __init__(self, n_arms: int = 10, epsilon: float = 0.1, alpha: float = 0.1):
        """
        Initialize agent with exponential recency-weighted averaging.
        
        Args:
            n_arms: Number of arms
            epsilon: Exploration rate
            alpha: Step size (learning rate) for updating estimates
        """
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.alpha = alpha
        
        # Initialize estimates and counts
        self.Q = np.zeros(n_arms)  # Value estimates
        self.action_counts = np.zeros(n_arms)
        
    def select_action(self) -> int:
        """Select action using epsilon-greedy strategy"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_arms)
        return np.random.choice(np.where(self.Q == self.Q.max())[0])
    
    def update(self, action: int, reward: float):
        """
        Update value estimates using constant step size
        """
        self.action_counts[action] += 1
        # Use constant step size (alpha) instead of 1/n
        self.Q[action] += self.alpha * (reward - self.Q[action])

def run_experiment(n_steps: int = 10000) -> Tuple[List[float], List[int], List[float]]:
    """
    Run experiment with non-stationary bandit and modified agent.
    
    Returns:
        Tuple of (rewards, optimal_actions, average_rewards)
    """
    bandit = NonStationaryBandit()
    agent = RecencyWeightedEpsilonGreedy(epsilon=0.1, alpha=0.1)
    
    rewards = []
    optimal_actions = []
    average_rewards = []
    total_reward = 0
    
    for step in range(n_steps):
        # Get optimal action based on true values
        optimal_action = np.argmax(bandit.q_values)
        
        # Select and take action
        action = agent.select_action()
        reward = bandit.get_reward(action)
        
        # Update agent
        agent.update(action, reward)
        
        # Track results
        rewards.append(reward)
        optimal_actions.append(1 if action == optimal_action else 0)
        total_reward += reward
        average_rewards.append(total_reward / (step + 1))
    
    return rewards, optimal_actions, average_rewards

# Run multiple experiments for more reliable results
def run_multiple_experiments(n_experiments: int = 10, n_steps: int = 10000):
    all_rewards = np.zeros((n_experiments, n_steps))
    all_optimal_actions = np.zeros((n_experiments, n_steps))
    
    for i in range(n_experiments):
        rewards, optimal_actions, _ = run_experiment(n_steps)
        all_rewards[i] = rewards
        all_optimal_actions[i] = optimal_actions
    
    # Calculate averages across experiments
    avg_rewards = np.mean(all_rewards, axis=0)
    avg_optimal = np.mean(all_optimal_actions, axis=0)
    
    # Plotting
    plt.figure(figsize=(15, 5))
    
    # Plot average reward
    plt.subplot(1, 2, 1)
    plt.plot(moving_average(avg_rewards, window=100))
    plt.xlabel('Time steps')
    plt.ylabel('Average Reward')
    plt.title('Average Reward over Time\n(Smoothed with 100-step window)')
    
    # Plot percentage of optimal actions
    plt.subplot(1, 2, 2)
    plt.plot(moving_average(avg_optimal * 100, window=100))
    plt.xlabel('Time steps')
    plt.ylabel('% Optimal Action')
    plt.title('Percentage of Optimal Actions\n(Smoothed with 100-step window)')
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print(f"Final average reward: {np.mean(avg_rewards[-1000:]):.3f}")
    print(f"Final optimal action percentage: {np.mean(avg_optimal[-1000:]) * 100:.1f}%")

def moving_average(data: np.ndarray, window: int = 100) -> np.ndarray:
    """Calculate moving average with specified window"""
    return np.convolve(data, np.ones(window) / window, mode='valid')

# Run the analysis
if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility
    run_multiple_experiments(n_experiments=10, n_steps=10000)
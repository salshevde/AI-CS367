import numpy as np
import matplotlib.pyplot as plt

class BinaryBandit:
    def __init__(self, p1, p2):
        """
        Initialize bandit with success probabilities for both arms
        p1: probability of success for arm 1
        p2: probability of success for arm 2
        """
        self.p1 = p1
        self.p2 = p2
    
    def pull(self, arm):
        """Pull the selected arm and return reward"""
        if arm == 1:
            return np.random.binomial(1, self.p1)
        else:
            return np.random.binomial(1, self.p2)

def epsilon_greedy(bandit, num_trials, epsilon):
    """
    Implement epsilon-greedy algorithm
    bandit: BinaryBandit instance
    num_trials: number of trials to run
    epsilon: exploration probability
    """
    # Initialize arrays to store results
    rewards = np.zeros(num_trials)
    actions = np.zeros(num_trials)
    
    # Initialize estimates and counts
    q_values = np.zeros(2)  # Estimated value for each arm
    n_values = np.zeros(2)  # Number of times each arm was pulled
    
    cumulative_rewards = np.zeros(num_trials)
    average_rewards = np.zeros(num_trials)
    
    for t in range(num_trials):
        # Epsilon-greedy action selection
        if np.random.random() < epsilon:
            action = np.random.randint(1, 3)  # Explore (random action between 1 and 2)
        else:
            action = np.argmax(q_values) + 1  # Exploit (best action)
        
        # Get reward
        reward = bandit.pull(action)
        
        # Update counts and estimates
        action_idx = action - 1
        n_values[action_idx] += 1
        q_values[action_idx] += (reward - q_values[action_idx]) / n_values[action_idx]
        
        # Store results
        rewards[t] = reward
        actions[t] = action
        
        # Calculate cumulative and average rewards
        cumulative_rewards[t] = np.sum(rewards[:t+1])
        average_rewards[t] = cumulative_rewards[t] / (t + 1)
    
    return rewards, actions, cumulative_rewards, average_rewards

def plot_results(average_rewards, cumulative_rewards, num_trials):
    """Plot the results of the epsilon-greedy algorithm"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot average reward
    ax1.plot(range(num_trials), average_rewards)
    ax1.set_xlabel('Trials')
    ax1.set_ylabel('Average Reward')
    ax1.set_title('Average Reward over Time')
    ax1.grid(True)
    
    # Plot cumulative reward
    ax2.plot(range(num_trials), cumulative_rewards)
    ax2.set_xlabel('Trials')
    ax2.set_ylabel('Cumulative Reward')
    ax2.set_title('Cumulative Reward over Time')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# Run simulation
if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Choose which binary bandit to use (A or B)
    # For binaryBanditA:
    p1_A = 0.1  # Probability of success for arm 1
    p2_A = 0.2  # Probability of success for arm 2
    
    # For binaryBanditB:
    p1_B = 0.8  # Probability of success for arm 1
    p2_B = 0.9  # Probability of success for arm 2
    
    # Initialize bandit A or B
    bandit_choice = "A"  # Change to "B" for binaryBanditB
    if bandit_choice == "A":
        bandit = BinaryBandit(p1_A, p2_A)
    else:
        bandit = BinaryBandit(p1_B, p2_B)
    
    # Set parameters
    num_trials = 1000
    epsilon = 0.1
    
    # Run epsilon-greedy algorithm
    rewards, actions, cumulative_rewards, average_rewards = epsilon_greedy(bandit, num_trials, epsilon)
    
    # Plot results
    plot_results(average_rewards, cumulative_rewards, num_trials)

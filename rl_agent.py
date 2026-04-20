"""
InsurGuard Reinforcement Learning Agent
Q-Learning agent for dynamic insurance policy adjustments
"""

import numpy as np
from typing import Dict, Tuple, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PolicyAdjustmentAgent:
    """Q-Learning agent for dynamic premium adjustments"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95,
                 epsilon: float = 1.0, epsilon_decay: float = 0.995):
        """
        Initialize Q-Learning agent
        
        Args:
            learning_rate: Alpha parameter for Q-learning updates
            discount_factor: Gamma parameter for future rewards
            epsilon: Exploration probability
            epsilon_decay: Rate of exploration decay
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = 0.01
        
        # State discretization
        self.bmi_bins = 10
        self.age_bins = 10
        self.smoking_states = 2  # smoker/non-smoker
        
        # Q-table: (bmi_state, age_state, smoking_state, action) -> Q_value
        # Actions: 0=reduce_premium, 1=maintain, 2=increase_premium
        self.q_table = {}
        
        self.episode_rewards = []
        self.training_history = []
        
        logger.info("Q-Learning agent initialized")
    
    def _discretize_state(self, bmi: float, age: float, smoker: int) -> Tuple:
        """Convert continuous features to discrete state"""
        # Bin age: 18-65
        age_state = min(self.age_bins - 1, max(0, int((age - 18) / 47 * self.age_bins)))
        
        # Bin BMI: 15-55
        bmi_state = min(self.bmi_bins - 1, max(0, int((bmi - 15) / 40 * self.bmi_bins)))
        
        return (bmi_state, age_state, smoker)
    
    def _calculate_reward(self, predicted_charge: float, optimal_charge: float,
                         customer_satisfaction: float) -> float:
        """
        Calculate reward for policy adjustment
        
        Args:
            predicted_charge: ML model's predicted charge
            optimal_charge: Suggested charge based on RL logic
            customer_satisfaction: Satisfaction score (0-1)
            
        Returns:
            Reward value
        """
        # Balance between profit and customer satisfaction
        profit_margin = (optimal_charge - predicted_charge) / predicted_charge if predicted_charge > 0 else 0
        
        # Reward components
        profit_reward = profit_margin * 100  # Scale profit component
        satisfaction_reward = customer_satisfaction * 50
        
        total_reward = profit_reward + satisfaction_reward
        return float(total_reward)
    
    def select_action(self, state: Tuple, is_training: bool = True) -> int:
        """
        Select action using epsilon-greedy strategy
        
        Args:
            state: Discretized state tuple
            is_training: Whether in training mode
            
        Returns:
            Action index (0=reduce, 1=maintain, 2=increase)
        """
        if is_training and np.random.random() < self.epsilon:
            return np.random.randint(0, 3)  # Explore
        else:
            # Exploit: choose best action from Q-table
            if state not in self.q_table:
                self.q_table[state] = [0.0, 0.0, 0.0]
            return np.argmax(self.q_table[state])
    
    def update_q_value(self, state: Tuple, action: int, reward: float,
                      next_state: Tuple):
        """
        Update Q-value using Q-Learning update rule
        
        Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
        """
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0]
        
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0, 0.0, 0.0]
        
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state])
        
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[state][action] = new_q
    
    def train_episode(self, health_metrics: List[Dict], ml_predictions: np.ndarray,
                     base_satisfaction: float = 0.8) -> float:
        """
        Run single training episode
        
        Args:
            health_metrics: List of customer health data dicts
            ml_predictions: ML model predictions for charges
            base_satisfaction: Starting customer satisfaction
            
        Returns:
            Episode reward sum
        """
        episode_reward = 0.0
        
        for idx, metrics in enumerate(health_metrics):
            # Current state
            state = self._discretize_state(
                metrics.get('bmi', 25),
                metrics.get('age', 30),
                metrics.get('smoker', 0)
            )
            
            # Select action
            action = self.select_action(state, is_training=True)
            
            # Get next state (assume slight change in health metrics)
            next_bmi = metrics.get('bmi', 25) + np.random.normal(0, 0.5)
            next_age = min(metrics.get('age', 30) + 1, 65)  # Age increases
            next_smoker = metrics.get('smoker', 0)
            next_state = self._discretize_state(next_bmi, next_age, next_smoker)
            
            # Apply action and calculate new charge
            ml_prediction = ml_predictions[idx]
            action_multipliers = [0.95, 1.0, 1.05]  # reduce, maintain, increase
            adjusted_charge = ml_prediction * action_multipliers[action]
            
            # Calculate satisfaction based on adjustment
            satisfaction = base_satisfaction * (1 - abs(action - 1) * 0.1)  # Penalty for extreme actions
            
            # Calculate reward
            reward = self._calculate_reward(ml_prediction, adjusted_charge, satisfaction)
            episode_reward += reward
            
            # Update Q-value
            self.update_q_value(state, action, reward, next_state)
        
        # Decay exploration rate
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        self.episode_rewards.append(episode_reward)
        return episode_reward
    
    def adjust_premium(self, bmi: float, age: float, smoker: int,
                      predicted_charge: float) -> Dict:
        """
        Use trained agent to adjust premium
        
        Args:
            bmi: Customer BMI
            age: Customer age
            smoker: 1 if smoker, 0 otherwise
            predicted_charge: ML model prediction
            
        Returns:
            Dictionary with adjustment details
        """
        state = self._discretize_state(bmi, age, smoker)
        action = self.select_action(state, is_training=False)
        
        action_multipliers = [0.95, 1.0, 1.05]
        adjustment_factor = action_multipliers[action]
        adjusted_charge = predicted_charge * adjustment_factor
        
        actions_desc = ['REDUCE (5%)', 'MAINTAIN', 'INCREASE (5%)']
        
        return {
            'original_charge': float(predicted_charge),
            'adjusted_charge': float(adjusted_charge),
            'adjustment_factor': float(adjustment_factor),
            'action': actions_desc[action],
            'policy_change': f"{(adjustment_factor - 1) * 100:+.1f}%"
        }
    
    def get_training_summary(self) -> Dict:
        """Get agent training statistics"""
        if not self.episode_rewards:
            return {}
        
        return {
            'episodes_trained': len(self.episode_rewards),
            'total_reward': float(np.sum(self.episode_rewards)),
            'average_reward': float(np.mean(self.episode_rewards)),
            'max_reward': float(np.max(self.episode_rewards)),
            'q_table_size': len(self.q_table),
            'final_epsilon': float(self.epsilon),
            'reward_trend': self.episode_rewards[-10:] if len(self.episode_rewards) >= 10 else self.episode_rewards
        }

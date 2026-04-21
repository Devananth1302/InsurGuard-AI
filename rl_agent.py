import numpy as np
import pickle
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PolicyAdjustmentAgent:

    def __init__(self,
                 learning_rate=0.1,
                 discount_factor=0.95,
                 epsilon=0.1,
                 q_table_path="saved_models/q_table.pkl"):

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table_path = q_table_path

        self.q_table = self._load_q_table()

        self.bmi_bins = 10
        self.age_bins = 10

    # ================= LOAD / SAVE =================

    def _load_q_table(self):
        if os.path.exists(self.q_table_path):
            with open(self.q_table_path, "rb") as f:
                logger.info("✅ Loaded Q-table")
                return pickle.load(f)
        return {}

    def save_q_table(self):
        os.makedirs(os.path.dirname(self.q_table_path), exist_ok=True)
        with open(self.q_table_path, "wb") as f:
            pickle.dump(self.q_table, f)
        logger.info("💾 Q-table saved")

    # ================= CORE =================

    def _discretize_state(self, bmi, age, smoker):
        age_state = min(self.age_bins - 1, max(0, int((age - 18) / 47 * self.age_bins)))
        bmi_state = min(self.bmi_bins - 1, max(0, int((bmi - 15) / 40 * self.bmi_bins)))
        return (bmi_state, age_state, int(smoker))

    def select_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0]

        if np.random.random() < self.epsilon:
            return np.random.randint(0, 3)

        return int(np.argmax(self.q_table[state]))

    def update_q(self, state, action, reward, next_state):
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0, 0.0, 0.0]

        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state])

        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )

    # ================= MAIN =================

    def adjust_premium(self, bmi, age, smoker, predicted_charge):

        state = self._discretize_state(bmi, age, smoker)
        action = self.select_action(state)

        multipliers = [0.95, 1.0, 1.05]
        factor = multipliers[action]
        adjusted = predicted_charge * factor

        # 🔥 SIMPLE ONLINE LEARNING
        reward = (adjusted - predicted_charge) * 0.01

        next_state = self._discretize_state(bmi, age + 1, smoker)

        self.update_q(state, action, reward, next_state)

        # Save learning
        self.save_q_table()

        actions_desc = ['REDUCE (5%)', 'MAINTAIN', 'INCREASE (5%)']

        return adjusted, factor, actions_desc[action]
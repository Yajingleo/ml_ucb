import numpy as np

class MLUCBMABSimulation:
    def __init__(self, user_matrix, item_matrix, rating_matrix, alpha=1.0):
        """
        user_matrix: np.ndarray of shape (n_user, n_feature)
        item_matrix: np.ndarray of shape (n_item, n_feature)
        rating_matrix: np.ndarray of shape (n_user, n_item)
        alpha: exploration parameter for UCB
        """
        self.user_matrix = user_matrix
        self.item_matrix = item_matrix
        self.rating_matrix = rating_matrix
        self.n_user = user_matrix.shape[0]
        self.n_item = item_matrix.shape[0]
        self.alpha = alpha
        self.counts = np.zeros((self.n_user, self.n_item))  # Number of times each arm is pulled
        self.rewards = np.zeros((self.n_user, self.n_item)) # Cumulative rewards

    def compute_ucb(self, user_idx):
        """
        Compute UCB scores for all items for a given user.
        """
        mean_rewards = np.zeros(self.n_item)
        uncertainty = np.zeros(self.n_item)
        for item_idx in range(self.n_item):
            if self.counts[user_idx, item_idx] > 0:
                mean_rewards[item_idx] = self.rewards[user_idx, item_idx] / self.counts[user_idx, item_idx]
                uncertainty[item_idx] = self.alpha * np.sqrt(
                    np.log(np.sum(self.counts[user_idx, :]) + 1) / (self.counts[user_idx, item_idx])
                )
            else:
                mean_rewards[item_idx] = 0
                uncertainty[item_idx] = np.inf  # Encourage exploration
        ucb_scores = mean_rewards + uncertainty
        return ucb_scores

    def recommend(self, user_idx):
        """
        Recommend the item with the highest UCB score for the user.
        """
        ucb_scores = self.compute_ucb(user_idx)
        return np.argmax(ucb_scores)

    def simulate(self, n_rounds=1000):
        """
        Run the simulation for n_rounds.
        """
        for round in range(n_rounds):
            user_idx = np.random.randint(self.n_user)
            item_idx = self.recommend(user_idx)
            reward = self.rating_matrix[user_idx, item_idx]
            self.counts[user_idx, item_idx] += 1
            self.rewards[user_idx, item_idx] += reward
            # Optionally update embeddings/model here

# Example usage:
# sim = MLUCBMABSimulation(user_matrix, item_matrix, rating_matrix)
# sim.simulate(n_rounds=1000)

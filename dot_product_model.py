import numpy as np
import pandas as pd
import seaborn as sns
import random
from typing import Tuple, List
import matplotlib.pyplot as plt


class DotProductModel:
    """
    Encapsulates the dot product model for collaborative filtering.
    Holds user and item matrices and provides methods for rating computation.
    """
    def __init__(self, n_item=100, n_user=100, n_feature=10, max_rating=10):
        self.n_item = n_item
        self.n_user = n_user
        self.n_feature = n_feature
        self.max_rating = max_rating
        self.item_matrix = None
        self.user_matrix = None
        self.rating_matrix = None
        self.has_rated_matrix = None
        self.rating_df = None

    def generate_user_preference(self):
        return np.random.random([self.n_user, self.n_feature])

    def generate_item_feature(self):
        return np.random.random([self.n_item, self.n_feature])

    def compute_item_rating(self, user_matrix, item_matrix):
        rating_matrix = item_matrix.dot(user_matrix.T)
        max_rating = rating_matrix.max()
        rating_matrix = np.round(rating_matrix / max_rating * self.max_rating)
        return rating_matrix

    def build_rating_df(self, rating_matrix, is_rated_matrix):
        item_inds, user_inds, ratings = [], [], []
        m, n = rating_matrix.shape
        for i in range(m):
            for j in range(n):
                if is_rated_matrix[i][j]:
                    item_inds.append(i)
                    user_inds.append(j)
                    ratings.append(rating_matrix[i][j])
        return pd.DataFrame({"user_ind": user_inds, "item_ind": item_inds, "rating": ratings})

    def parse_rating(self, rating_df, n_lines=0):
        if not set(["item_ind", "user_ind", "rating"]).issubset(rating_df.columns):
            raise ValueError('rating_df must have columns "item_ind", "user_ind", "rating"')
        rating_df = rating_df[["item_ind", "user_ind", "rating"]]
        if n_lines:
            rating_df = rating_df.head(n_lines)
        unique_item_inds = sorted(rating_df.item_ind.unique())
        unique_user_inds = sorted(rating_df.user_ind.unique())
        n_item = len(unique_item_inds)
        n_user = len(unique_user_inds)
        item_inds_map = {unique_item_inds[i]: i for i in range(n_item)}
        user_inds_map = {unique_user_inds[i]: i for i in range(n_user)}
        rating_mat = np.zeros([n_item, n_user])
        has_rated_mat = np.zeros([n_item, n_user])
        for item_ind, user_ind, rating in rating_df.values:
            row_ind = item_inds_map[item_ind]
            col_ind = user_inds_map[user_ind]
            rating_mat[row_ind][col_ind] = rating
            has_rated_mat[row_ind][col_ind] = 1
        return rating_mat, has_rated_mat


class SGDTrainer:
    """
    Trains the DotProductModel using SGD. Handles data loading and training.
    """
    def __init__(self, model: DotProductModel):
        self.model = model
        self.training_loss = None
        self.fitted_item_matrix = None
        self.fitted_user_matrix = None
        self.fitted_rating_matrix = None

    def LoadData(self):
        """
        Generate synthetic data and initialize model matrices.
        """
        self.model.item_matrix = self.model.generate_item_feature()
        self.model.user_matrix = self.model.generate_user_preference()
        self.model.rating_matrix = self.model.compute_item_rating(self.model.user_matrix, self.model.item_matrix)
        self.model.has_rated_matrix = np.round(np.random.random([self.model.n_item, self.model.n_user]))
        self.model.rating_df = self.model.build_rating_df(self.model.rating_matrix, self.model.has_rated_matrix)

    def TrainModel(self, mini_batch=1, eta=0.1, lambda_=0, n_epoch=10000):
        """
        Train the model using SGD and store fitted matrices and training loss.
        """
        n_feature = self.model.n_feature
        rating_df = self.model.rating_df
        n_item = len(set(rating_df.item_ind))
        n_user = len(set(rating_df.user_ind))
        rating_matrix, has_rated_matrix = self.model.parse_rating(rating_df)
        args = (rating_matrix, has_rated_matrix, lambda_, n_item, n_user, n_feature, mini_batch)
        item_matrix = np.random.rand(n_item, n_feature)
        user_matrix = np.random.rand(n_user, n_feature)
        self.training_loss = self.sgd(item_matrix, user_matrix, rating_df, eta, args, n_epoch)
        self.fitted_item_matrix = item_matrix
        self.fitted_user_matrix = user_matrix
        self.fitted_rating_matrix = np.round(self.fitted_item_matrix.dot(self.fitted_user_matrix.T))

    def point_loss(self, item_matrix, user_matrix, args):
        rating_matrix, has_rated_matrix, lambda_, n_item, n_user, n_feature, mini_batch = args
        estimated_matrix = item_matrix.dot(user_matrix.T)
        error_matrix = (estimated_matrix - rating_matrix) * has_rated_matrix
        return error_matrix * error_matrix

    def total_loss(self, item_matrix, user_matrix, args):
        rating_matrix, has_rated_matrix, lambda_, n_item, n_user, n_feature, mini_batch = args
        return self.point_loss(item_matrix, user_matrix, args).sum() / has_rated_matrix.sum()

    def update_gradient(self, item_matrix, user_matrix, rating_df, eta, args):
        rating_matrix, has_rated_matrix, lambda_, n_item, n_user, n_feature, mini_batch = args
        item_inds = rating_df.item_ind.values
        user_inds = rating_df.user_ind.values
        ratings = rating_df.rating.values
        grad_item = np.zeros(n_feature)
        grad_user = np.zeros(n_feature)
        for i in range(len(ratings)):
            item_ind, user_ind, rating = item_inds[i], user_inds[i], ratings[i]
            ind_i = int(item_ind)
            ind_u = int(user_ind)
            rating_matrix[ind_i][ind_u] = rating
            has_rated_matrix[ind_i][ind_u] = 1
            item_i = item_matrix[ind_i].copy()
            user_u = user_matrix[ind_u].copy()
            grad_item += (user_u.dot(item_i) - rating) * user_u + lambda_ * item_i
            grad_user += (user_u.dot(item_i) - rating) * item_i + lambda_ * user_u
            item_matrix[ind_i] = item_i - grad_item * eta / mini_batch
            user_matrix[ind_u] = user_u - grad_user * eta / mini_batch

    def sgd(self, item_matrix, user_matrix, rating_df, eta, args, n_epoch=0):
        rating_matrix, has_rated_matrix, lambda_, n_item, n_user, n_feature, mini_batch = args
        n_rating = rating_df.shape[0]
        indices = list(range(n_rating))
        random.shuffle(indices)
        training_loss = pd.DataFrame()
        n_epoch = n_epoch if n_epoch else len(indices) // mini_batch
        for i in range(n_epoch):
            row_start = (i * mini_batch) % n_rating
            row_end = ((i + 1) * mini_batch) % n_rating
            mini_batch_rating_df = rating_df.iloc[row_start:row_end]
            self.update_gradient(item_matrix, user_matrix, mini_batch_rating_df, eta, args)
            if i % 10 == 0:
                mini_batch_training_loss = pd.DataFrame({
                    "epoch": [i],
                    "loss": [self.total_loss(item_matrix, user_matrix, args)]
                })
                training_loss = pd.concat([training_loss, mini_batch_training_loss], ignore_index=True)
        return training_loss

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        sns.heatmap(self.model.rating_matrix)
        plt.title("Original Rating Matrix")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.lineplot(x="epoch", y="loss", data=self.training_loss)
        plt.title("Training Loss Curve")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.heatmap(self.model.has_rated_matrix)
        plt.title("Has Rated Matrix")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.heatmap(self.model.item_matrix.dot(self.model.user_matrix.T) * self.model.has_rated_matrix)
        plt.title("Predicted Ratings (Masked)")
        plt.show()

        self.training_loss["log_loss"] = np.log(self.training_loss.loss)
        self.training_loss["log_epoch"] = np.log(self.training_loss.epoch)
        self.training_loss.drop(0, inplace=True)
        plt.figure(figsize=(10, 6))
        sns.regplot(x="log_epoch", y="log_loss", data=self.training_loss)
        plt.title("Log-Transformed Training Loss vs Epoch")
        plt.show()

    def fit_linear_regression(self):
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(self.training_loss[["log_epoch"]], self.training_loss.log_loss)
        return model.coef_

    def fitting_error(self):
        return (np.linalg.norm((self.fitted_rating_matrix - self.model.rating_matrix) * self.model.has_rated_matrix) / self.fitted_rating_matrix.size) ** 0.5

    def item_feature_error(self):
        return (np.linalg.norm((self.fitted_item_matrix - self.model.item_matrix)) / self.model.item_matrix.size) ** 0.5


# Usage example:
model = DotProductModel()
trainer = SGDTrainer(model)
trainer.LoadData()
trainer.TrainModel()
trainer.plot_results()
print("Fitting error:", trainer.fitting_error())
print("Item feature error:", trainer.item_feature_error())
plot = trainer.fit_linear_regression()
print("Convergence rate (slope):", plot)

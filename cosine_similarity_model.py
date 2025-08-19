import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict

class CosineSimilarityRecommender:
    def __init__(self):
        self.user_ratings = defaultdict(dict)
        self.similarity_matrix = {}
        
    def add_rating(self, user_id: int, item_id: int, rating: float) -> None:
        """Add a user-item rating to the system"""
        self.user_ratings[user_id][item_id] = rating
        
    def compute_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        if len(vector1) == 0 or len(vector2) == 0:
            return 0.0
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
        
    def build_similarity_matrix(self) -> None:
        """Build user-user similarity matrix"""
        users = list(self.user_ratings.keys())
        
        for i in range(len(users)):
            user1 = users[i]
            self.similarity_matrix[user1] = {}
            
            for j in range(len(users)):
                user2 = users[j]
                
                # Get common items rated by both users
                items1 = set(self.user_ratings[user1].keys())
                items2 = set(self.user_ratings[user2].keys())
                common_items = items1.intersection(items2)
                
                # Create rating vectors for common items
                vector1 = np.array([self.user_ratings[user1][item] for item in common_items])
                vector2 = np.array([self.user_ratings[user2][item] for item in common_items])
                
                # Compute similarity
                similarity = self.compute_similarity(vector1, vector2)
                self.similarity_matrix[user1][user2] = similarity
                
    def get_recommendations(self, user_id: int, n_recommendations: int = 5) -> List[Tuple[int, float]]:
        """Get top N recommendations for a user"""
        if user_id not in self.similarity_matrix:
            return []
            
        # Find similar users
        similar_users = [(other_user, sim) 
                        for other_user, sim in self.similarity_matrix[user_id].items()
                        if other_user != user_id]
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        # Get items rated by similar users but not by target user
        recommendations = defaultdict(float)
        user_items = set(self.user_ratings[user_id].keys())
        
        for similar_user, similarity in similar_users:
            for item, rating in self.user_ratings[similar_user].items():
                if item not in user_items:
                    recommendations[item] += similarity * rating
                    
        # Sort and return top N recommendations
        sorted_recommendations = sorted(recommendations.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)
        return sorted_recommendations[:n_recommendations]

# Example usage
if __name__ == "__main__":
    recommender = CosineSimilarityRecommender()
    
    # Add some sample ratings
    recommender.add_rating(1, 1, 5.0)
    recommender.add_rating(1, 2, 3.0)
    recommender.add_rating(1, 3, 4.0)
    recommender.add_rating(2, 1, 3.0)
    recommender.add_rating(2, 2, 4.0)
    recommender.add_rating(2, 4, 5.0)
    recommender.add_rating(3, 1, 4.0)
    recommender.add_rating(3, 3, 5.0)
    recommender.add_rating(3, 4, 2.0)
    
    # Build similarity matrix
    recommender.build_similarity_matrix()
    
    # Get recommendations for user 1
    recommendations = recommender.get_recommendations(1, n_recommendations=2)
    print(f"Recommendations for user 1: {recommendations}")
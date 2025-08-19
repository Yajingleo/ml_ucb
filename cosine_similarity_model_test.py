import pytest
import numpy as np
from cosine_similarity_model import CosineSimilarityRecommender

class TestCosineSimilarityRecommender:
    @pytest.fixture
    def recommender(self):
        """Create a recommender instance with sample data"""
        rec = CosineSimilarityRecommender()
        # Add test ratings
        rec.add_rating(1, 1, 5.0)
        rec.add_rating(1, 2, 3.0)
        rec.add_rating(1, 3, 4.0)
        rec.add_rating(2, 1, 3.0)
        rec.add_rating(2, 2, 4.0)
        rec.add_rating(2, 4, 5.0)
        rec.add_rating(3, 1, 4.0)
        rec.add_rating(3, 3, 5.0)
        rec.add_rating(3, 4, 2.0)
        return rec

    def test_add_rating(self, recommender):
        """Test adding a rating"""
        recommender.add_rating(4, 1, 3.5)
        assert recommender.user_ratings[4][1] == 3.5

    def test_compute_similarity(self, recommender):
        """Test cosine similarity computation"""
        vector1 = np.array([1, 2, 3])
        vector2 = np.array([2, 4, 6])
        similarity = recommender.compute_similarity(vector1, vector2)
        assert np.isclose(similarity, 1.0)  # Should be perfectly correlated

    def test_empty_vectors_similarity(self, recommender):
        """Test similarity with empty vectors"""
        vector1 = np.array([])
        vector2 = np.array([])
        similarity = recommender.compute_similarity(vector1, vector2)
        assert similarity == 0.0

    def test_build_similarity_matrix(self, recommender):
        """Test building similarity matrix"""
        recommender.build_similarity_matrix()
        # Check if similarity matrix contains all users
        assert set(recommender.similarity_matrix.keys()) == {1, 2, 3}
        # Check if self-similarity is 1.0
        assert np.isclose(recommender.similarity_matrix[1][1], 1.0)

    def test_get_recommendations(self, recommender):
        """Test getting recommendations"""
        recommender.build_similarity_matrix()
        recommendations = recommender.get_recommendations(1, n_recommendations=1)
        assert len(recommendations) == 1
        # Item 4 should be recommended as it's rated highly by similar users
        assert recommendations[0][0] == 4

    def test_get_recommendations_unknown_user(self, recommender):
        """Test recommendations for unknown user"""
        recommender.build_similarity_matrix()
        recommendations = recommender.get_recommendations(999)
        assert recommendations == []
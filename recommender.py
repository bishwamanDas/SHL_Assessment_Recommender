# recommender.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SHLRecommender:
    def __init__(self, file_path="assessments_data.xlsx"):  # ✅ Default filename
        # Load data
        self.df = pd.read_excel(file_path)
        self.df.fillna("", inplace=True)

        # ✅ Combine more fields into one text column
        self.df["text"] = (
            self.df["Assessment Name"].astype(str) + " " +
            self.df["Test Type"].astype(str) + " " +
            self.df["Duration"].astype(str) + " " +
            self.df["Remote Testing Support"].astype(str) + " " +
            self.df["Adaptive/IRT Support"].astype(str)
        ).str.lower()

        # TF-IDF setup
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["text"])

    def recommend(self, query, top_k=10):
        # Handle empty or whitespace-only queries
        if not query or not query.strip():
            return pd.DataFrame()

        # Transform query and calculate cosine similarity
        query_vec = self.vectorizer.transform([query.lower()])
        scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        # Get top k matches
        top_indices = scores.argsort()[::-1][:top_k]
        return self.df.iloc[top_indices].copy()

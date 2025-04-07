from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import SHLRecommender
import pandas as pd

app = FastAPI(title="SHL Assessment Recommendation API")

# Enable CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the recommender with the correct Excel file
recommender = SHLRecommender("assessments_data.xlsx")

@app.get("/recommend")
def get_recommendations(query: str = Query(..., description="Job role, skill, or test requirement")):
    # Get recommendations from recommender
    results_df = recommender.recommend(query)

    # Check if recommendations are found
    if results_df.empty:
        return {"message": "No recommendations found", "results": []}

    # Format the results as a list of dictionaries for API response
    results = []
    for _, row in results_df.iterrows():
        results.append({
            "assessment_name": row["Assessment Name"],
            "url": row["URL"],
            "remote_testing": row["Remote Testing Support"],
            "adaptive_irt": row["Adaptive/IRT Support"],
            "duration": row["Duration"],
            "test_type": row["Test Type"]
        })

    # Return the query and matching assessments
    return {"query": query, "results": results}

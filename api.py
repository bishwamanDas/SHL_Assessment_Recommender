from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import SHLRecommender

app = FastAPI(title="SHL Assessment Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = SHLRecommender("assessments_data.xlsx")

@app.get("/recommend")
def get_recommendations(query: str = Query(...)):
    results_df = recommender.recommend(query)

    if results_df.empty:
        return {"message": "No recommendations found", "results": []}

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

    return {"query": query, "results": results}

from recommender import SHLRecommender

# Initialize the recommender with the correct file
recommender = SHLRecommender("assessments_data.xlsx")

# Sample queries
queries = [
    "Hiring a Java backend developer",
    "Looking for data analyst with SQL and Excel",
    "Need someone for customer support role",
    "Mid-level software engineer, Python and JS",
    "Finance and bookkeeping test for accountant"
]

# Run and print recommendations
for query in queries:
    print(f"\n🔍 Query: {query}")
    results = recommender.recommend(query, top_k=5)

    if not results.empty:
        print(results[[
            "Assessment Name",
            "URL",
            "Remote Testing Support",
            "Adaptive/IRT Support",
            "Duration",
            "Test Type"
        ]].to_string(index=False))
    else:
        print("No recommendations found.")

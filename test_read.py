from recommender import recommend
import pandas as pd

# Sample queries to test the recommendation engine
queries = [
    "Hiring a Java backend developer",
    "Looking for data analyst with SQL and Excel",
    "Need someone for customer support role",
    "Mid-level software engineer, Python and JS",
    "Finance and bookkeeping test for accountant"
]

# Test each query
for query in queries:
    print(f"\n🔍 Query: {query}")
    
    # Get top 5 recommendations
    results = recommend(query, top_n=5)
    
    if not results.empty:
        # Show only the main columns
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

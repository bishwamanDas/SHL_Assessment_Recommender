import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- Keywords ---
DOMAIN_KEYWORDS = {
    "developer": ["java", "python", "developer", "software", "backend", "frontend", "programmer", "engineer"],
    "data": ["data", "analyst", "analytics", "sql", "machine learning", "statistics"],
    "sales": ["sales", "crm", "negotiation", "retail", "customer"],
    "support": ["support", "helpdesk", "service", "call center", "technical support"],
    "finance": ["account", "finance", "bookkeeping", "tax"],
    "manager": ["manager", "leadership", "project", "scrum", "product owner"]
}

SKILL_KEYWORDS = [
    "python", "sql", "java", "javascript", "c++", "html", "css",
    "aws", "react", "node", "django", "flask", "data analysis",
    "machine learning", "mongodb"
]

# --- Load model from local directory ---
model_path = os.path.join(os.path.dirname(__file__), 'all-MiniLM-L6-v2')
model = SentenceTransformer(model_path)

# --- Utilities ---
def extract_query_domain(query):
    query = query.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(word in query for word in keywords):
            return domain
    return "general"

def extract_skills(query):
    return [skill for skill in SKILL_KEYWORDS if skill in query.lower()]

def extract_expected_duration(query):
    match = re.search(r'(\d+)\s*(min|minutes)', query.lower())
    return int(match.group(1)) if match else None

# --- Load and preprocess data ---
file_path = os.path.join(os.path.dirname(__file__), "assessments_data.xlsx")
df = pd.read_excel(file_path)
df.fillna("Unknown", inplace=True)

df['Tags'] = df['Tags'].astype(str)
df['tags_list'] = df['Tags'].apply(lambda x: [tag.strip().lower() for tag in x.split(",")])
df['combined'] = df['Assessment Name'] + " " + df['Tags']

df['embedding'] = df['combined'].apply(lambda x: model.encode(x, convert_to_tensor=False))

# --- Recommend Function ---
def recommend(query, top_n=10):
    domain = extract_query_domain(query)
    skills = extract_skills(query)
    expected_duration = extract_expected_duration(query)

    # Domain filter
    def match_domain(row):
        combined = row['Assessment Name'].lower() + " " + row['Tags'].lower()
        return any(word in combined for word in DOMAIN_KEYWORDS[domain]) if domain != "general" else True

    filtered_df = df[df.apply(match_domain, axis=1)].reset_index(drop=True)

    # Skill filter
    def match_skill(row):
        text = (row['Assessment Name'] + " " + row['Tags']).lower()
        return any(skill in text for skill in skills)

    skill_df = filtered_df[filtered_df.apply(match_skill, axis=1)].reset_index(drop=True)
    if not skill_df.empty:
        filtered_df = skill_df

    # Duration filter (±15 mins)
    if expected_duration:
        filtered_df = filtered_df[
            filtered_df['Duration (in minutes)'].apply(lambda d: abs(d - expected_duration) <= 15)
        ].reset_index(drop=True)

    if filtered_df.empty:
        return pd.DataFrame([{
            "Assessment Name": "No relevant assessments found",
            "URL": "",
            "Remote Testing Support": "",
            "Adaptive/IRT Support": "",
            "Duration (in minutes)": "",
            "Test Type": ""
        }])

    # Embedding similarity
    query_vec = model.encode(query, convert_to_tensor=False)
    emb_matrix = np.vstack(filtered_df['embedding'].values)
    emb_scores = cosine_similarity([query_vec], emb_matrix)[0]

    # Skill score
    def skill_score(row):
        text = (row['Assessment Name'] + " " + row['Tags']).lower()
        return sum(skill in text for skill in skills)

    skill_scores = filtered_df.apply(skill_score, axis=1)

    # Duration score
    def duration_score(row):
        if expected_duration:
            diff = abs(row['Duration (in minutes)'] - expected_duration)
            return max(0, 1 - diff / 15)
        return 0

    duration_scores = filtered_df.apply(duration_score, axis=1)

    # Final score
    final_scores = 0.2 * emb_scores + 0.5 * skill_scores + 0.3 * duration_scores
    top_indices = np.argsort(-final_scores)[:top_n]

    return filtered_df.iloc[top_indices][[
        "Assessment Name", "URL", "Remote Testing Support",
        "Adaptive/IRT Support", "Duration (in minutes)", "Test Type"
    ]]

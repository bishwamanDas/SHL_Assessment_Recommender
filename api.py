import streamlit as st
import requests

# FastAPI URL for recommendations (replace with your deployed FastAPI URL)
API_URL = "https://shl-api-3t3h.onrender.com"

# Streamlit UI setup
st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🧠")
st.title("🔍 SHL Assessment Recommender")

# Input box for user query
query = st.text_input("Enter job role, skill, or test requirement:")

# Function to fetch recommendations from FastAPI
def get_recommendations_from_api(query):
    url = f"{API_URL}?query={query}"
    response = requests.get(url)
    return response.json()  # Returns the response as a JSON

# Show results only when query is entered
if query.strip():
    # Fetch recommendations from FastAPI
    results = get_recommendations_from_api(query)

    # If results are returned, display them
    if results['results']:
        st.subheader("📋 Top 10 Matching Assessments:")
        for result in results['results']:
            st.markdown(f"**📝 {result['assessment_name']}**")
            st.write(f"- 📍 Assessment Name: {result['assessment_name']}")
            st.write(f"- 📍 Remote Testing: {result['remote_testing']}")
            st.write(f"- 📐 Adaptive/IRT: {result['adaptive_irt']}")
            st.write(f"- ⏱️ Duration: {result['duration']}")
            st.write(f"- 📚 Test Type: {result['test_type']}")
            st.write(f"- 🔗 URL: {result['url']}")
            st.markdown("---")
    else:
        st.warning("❗ No relevant assessments found. Try a broader or clearer query.")
else:
    st.info("💡 Please enter a job title, skills, or requirement above to see recommendations.")

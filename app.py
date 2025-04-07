# app.py
import streamlit as st
from recommender import SHLRecommender

# Initialize the recommender with the correct Excel file
recommender = SHLRecommender("assessments_data.xlsx")  # ✅ fixed filename

# Streamlit UI
st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🧠")
st.title("🔍 SHL Assessment Recommender ")

# Input box for user query
query = st.text_input("Enter job role, skill, or test requirement:")

# Show results only when query is entered
if query.strip():
    results = recommender.recommend(query)

    if not results.empty:
        st.subheader("📋 Top 10 Matching Assessments:")
        for _, row in results.iterrows():
            st.markdown(f"**📝 {row['Assessment Name']}**")
            st.write(f"- 📍 Assessment Name: {row['Assessment Name']}")
            st.write(f"- 📍 Remote Testing: {row['Remote Testing Support']}")
            st.write(f"- 📐 Adaptive/IRT: {row['Adaptive/IRT Support']}")
            st.write(f"- ⏱️ Duration: {row['Duration']}")
            st.write(f"- 📚 Test Type: {row['Test Type']}")
            st.write(f"- 🔗 URL: {row['URL']}")
            st.markdown("---")
    else:
        st.warning("❗ No relevant assessments found. Try a broader or clearer query.")
else:
    st.info("💡 Please enter a job title, skills, or requirement above to see recommendations.")

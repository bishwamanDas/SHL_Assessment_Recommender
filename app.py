# app.py

import streamlit as st
import pandas as pd
from recommender import recommend  # Import the recommend function from recommender.py

import os
print("Current Working Directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Page Setup
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommendation Engine")
st.markdown("Enter a job description or required skills to get relevant SHL assessment suggestions.")

# Input Box
query = st.text_input("Job Description or Skills:", placeholder="e.g. Backend Python developer, 45 min test")

# Recommendation Display Logic
def display_recommendations(results: pd.DataFrame):
    if len(results) == 1 and results.iloc[0]["Assessment Name"] == "No relevant assessments found":
        st.warning("❌ No relevant assessments found. Try rephrasing your query or using more specific skills or test durations.")
        return

    st.markdown("### 📋 Top Recommended Assessments:")
    for i, row in results.iterrows():
        with st.expander(f"{i+1}. {row['Assessment Name']}"):
            st.write(f"🔗 **Link:** [{row['URL']}]({row['URL']})")
            st.write(f"🧪 **Test Type:** {row['Test Type']}")
            st.write(f"⏱️ **Duration:** {row['Duration']}")
            st.write(f"🖥️ **Remote Testing Support:** {row['Remote Testing Support']}")
            st.write(f"📊 **Adaptive/IRT Support:** {row['Adaptive/IRT Support']}")

# Button trigger
if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("⚠️ Please enter a valid query.")
    else:
        try:
            results = recommend(query, top_n=10)
            display_recommendations(results)
        except Exception as e:
            st.error(f"❗ Something went wrong: {e}")

# Footer
st.markdown("<hr><center>🚀 Built for the SHL AI Internship Challenge</center>", unsafe_allow_html=True)

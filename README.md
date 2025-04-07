<SHL Assessment Recommender>

The SHL Assessment Recommender is a machine learning-based recommendation system built to suggest relevant SHL assessments based on a given job role, skill set, or test requirements. The system uses a combination of TF-IDF vectorization and cosine similarity to provide personalized recommendations.
This system is built using FastAPI, Streamlit, and scikit-learn for the backend API and frontend user interface. It is designed to help recruiters or hiring managers find the right SHL assessments for job applicants quickly and efficiently.

Features --
Text-based Querying: Enter a job description, skills, or test requirements.
Relevant Assessment Suggestions: Get a list of SHL assessments based on your query.
Easy-to-use UI: Streamlit-based user interface for querying and displaying results.
API for Integration: FastAPI-based REST API to get recommendations in JSON format.

Tools and Libraries Used --
Python: Main programming language for the project.
Streamlit: For building the frontend application.
FastAPI: For building the backend API to serve recommendations.
scikit-learn: For building the recommendation engine using TF-IDF and cosine similarity.
Pandas: For handling data.
openpyxl: For reading the Excel file containing assessment data.

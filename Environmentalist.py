import streamlit as st
import google.generativeai as genai
import os

# Set page title and header
st.title("Generate Content using Generative AI")

# Input for API Key
GOOGLE_API_KEY = st.text_input("Enter your Google API Key:")

# Input for user question
user_question = st.text_area("Enter your question:", "How to Save Environment")

if st.button("Generate Content"):
    if GOOGLE_API_KEY:
        # Configure the generative AI library
        genai.configure(api_key=GOOGLE_API_KEY)

        # Initialize the GenerativeModel
        model = genai.GenerativeModel('gemini-1.0-pro-latest')

        # Generate content based on user question
        response = model.generate_content(user_question)

        # Display generated content
        st.write(response.text)  # Use st.write() to display text content
    else:
        st.warning("Please enter your Google API Key.")

# Optional: Display some instructions or information about the app
st.markdown("This app uses Google Generative AI to generate content based on a user-provided question.")

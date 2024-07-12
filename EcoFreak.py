import streamlit as st
import google.generativeai as genai
import os

# Set page title and header with the chatbot name
st.title("EcoFreak - Your Environmentalist Chatbot using Generative AI")

# Input for API Key
GOOGLE_API_KEY = st.text_input("Enter your Google API Key:")

# Input for user question
user_question = st.text_area("Enter your question:", "How to Save Environment")

if st.button("Generate Response"):
    if GOOGLE_API_KEY:
        # Configure the generative AI library
        genai.configure(api_key=GOOGLE_API_KEY)

        # Initialize the GenerativeModel
        model = genai.GenerativeModel('gemini-1.0-pro-latest')

        # Generate content based on user question
        response = model.generate_content(user_question)

        # Adjust response for environmentalist dialect
        generated_text = response.text.replace("I", "EcoFreak")  # Adjusted for chatbot name

        # Display generated content with environmentalist dialect
        st.write(generated_text)
    else:
        st.warning("Please enter your Google API Key.")

# Optional: Display some instructions or information about the chatbot
st.markdown("EcoFreak is your chatbot powered by Google Generative AI, providing environmentally conscious responses based on your questions.")

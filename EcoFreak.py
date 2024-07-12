import streamlit as st
import google.generativeai as genai
import os

st.title("EcoFreak - Your Environmentalist Chatbot using Generative AI")

GOOGLE_API_KEY = st.text_input("Enter your Google API Key:")

user_question = st.text_area("Enter your question:", "How to Save Environment")

if st.button("Generate Response"):
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(user_question)
        generated_text = response.text.replace("I", "EcoFreak")  # Adjusted for chatbot name
        st.write(generated_text)
    else:
        st.warning("Please enter your Google API Key.")

st.markdown("EcoFreak is your chatbot powered by Google Generative AI, providing environmentally conscious responses based on your questions.")

import streamlit as st
import google.generativeai as genai
import cohere
from langchain import LLMChain
from langchain.llms import Cohere as LangchainCohere
from langchain.prompts import PromptTemplate
import tempfile
import base64
import requests
from PIL import Image
from io import BytesIO

# Keys 

# Google API Key: https://ai.google.dev/gemini-api/docs/api-key
GOOGLE_API_KEY = 'AIzaSyBXq-1xtb_0jNdhw-CdW7b7SLnghzrycaQ'

# Stability AI API Key: https://platform.stability.ai/account/keys
STABILITY_API_KEY = 'sk-z6Kj18xNpMMFVOo4O93z8cCrxcYgXzTSSnvw3jlmtJu0p35z'

# Cohere API Key: https://dashboard.cohere.com/api-keys
COHERE_API_KEY = "QLFI6zjXBG3iIxMCuw0WhHfuD7PtYit9uVLMOeBh"

# Gemini

# Generation configuration
generation_config = {
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 64,
    "max_output_tokens": 500,  
}

def generate_content(prompt):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
    response = model.generate_content(prompt)
    try:
        st.write(response.text)
    except Exception as e:
        st.error(f"Exception:\n {e} \n")
        st.write("Response:\n", response.candidates)

# Stability

def generate_image(prompt, api_key):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad",
                "weight": -1
            }
        ],
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        return None
    
    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    image = Image.open(BytesIO(image_data))
    return image

# Cohere

llm = LangchainCohere(cohere_api_key=COHERE_API_KEY)

prompt = PromptTemplate(template="Give advice on reducing carbon footprint in {context}.",
                        input_variables=["context"])

chain = LLMChain(llm=llm, prompt=prompt)

def get_advice(context):
    response = chain.run({"context": context})
    return response

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    # Menu
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Environmental Query", "Crop Disease Prediction", "Reduce Carbon Footprints", "Plant Care", "Future Imagination", "FAQ"])

    
    with tab1:
        st.header("Environmental Query")
        default_prompt = "How to Conserve Environment and How do I best take care of it?"
        user_text_question = st.text_input("Enter your question about environmental preservation:")
        user_text_question = user_text_question + default_prompt
        if st.button("Check how to Conserve"):
            if not user_text_question:
                st.error("Please enter a text question.")
            else:
                st.subheader("Environmental Conservation Result")
                generate_content(user_text_question)

    with tab2:
        st.header("Crop Disease Prediction")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        default_prompt = "Identify the disease for the crop and provide recommendation to cure the disease."
        if st.button("Detect Image"):
            if uploaded_file is None:
                st.warning("Please upload an image file.")
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Image', use_column_width=True)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name
                prompt_parts = [
                    genai.upload_file(temp_file_path),
                    default_prompt
                ]
                st.subheader("Crop Disease Prediction Result")
                generate_content(prompt_parts)

    with tab3:
        st.title("Reduce Carbon Footprints")
        st.write("Ask for advice on how to save the environment.")
        
        context = st.text_input("E.g. Home Energy Usage, Travel Habits")
        if context:
            advice = get_advice(context)
            st.write(advice)

    with tab4:        
        st.header("Plant Care")
        uploaded_file_plant = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"], key="btn_identify_plant")
        default_prompt = "Do you know what plant this is? How do I best take care of it?"
        if st.button("Identify Plant"):
            if uploaded_file_plant is None:
                st.warning("Please upload an image file.")
            else:
                image = Image.open(uploaded_file_plant)
                st.image(image, caption='Uploaded Image', use_column_width=True)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_file.write(uploaded_file_plant.getvalue())
                    temp_file_path = temp_file.name
                prompt_parts = [
                    genai.upload_file(temp_file_path),
                    default_prompt
                ]
                st.subheader("Plant Care Result")
                generate_content(prompt_parts)

    with tab5:
        st.header("Future Imagination")
        prompt = st.text_input("Enter your Future environment Imagination prompt:")
        if st.button("Generate Image"):
            if not prompt or not STABILITY_API_KEY:
                st.warning("Please provide both prompt and API key.")
            else:
                with st.spinner('Generating image...'):
                    image = generate_image(prompt, STABILITY_API_KEY)
                    if image:
                        st.image(image, caption='Generated Image', use_column_width=True)
                        # Save the image for download
                        img_buffer = BytesIO()
                        image.save(img_buffer, format='PNG')
                        img_buffer.seek(0)
                        b64_img = base64.b64encode(img_buffer.read()).decode()
                        href = f'<a href="data:file/png;base64,{b64_img}" download="generated_image.png">Download Image</a>'
                        st.markdown(href, unsafe_allow_html=True)

    with tab6:
        st.header("FAQ")
        st.write("""
        **1. How to use the Environmental Query tab?**
        - Enter your question about environmental preservation in the text input field.
        - Click on "Check how to Conserve" to get the result.

        **2. How to use the Crop Disease Prediction tab?**
        - Upload an image of the crop.
        - Click on "Detect Image" to get the disease prediction and recommendations.

        **3. How to use the Reduce Carbon Footprints tab?**
        - Enter the context in which you want advice on reducing carbon footprint.
        - The chatbot will provide tailored advice for your context.

        **4. How to use the Plant Care tab?**
        - Upload an image of the plant.
        - Click on "Identify Plant" to get information about the plant and care instructions.

        **5. How to use the Future Imagination tab?**
        - Enter an environment-related prompt.
        - Click on "Generate Image" to get an AI-generated image based on your prompt.
        """)
        st.write("**Video Tutorial**")
        st.video("https://youtu.be/XOCjPsALTcM")

else:
    st.error("Please enter a valid Google API key.")

# streamlit run Ecofreak_Bot.py

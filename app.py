## Invoice Extractor
from dotenv import load_dotenv

load_dotenv() ## load all env var from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

##configuring API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load gemini pro vision and get response
def get_gemini_response(input,image,prompt):
    ##load the model
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        ##convert the uploaded file to bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, #get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


#initialize our streamlit app

st.set_page_config(page_title="Invoice Extractor", page_icon=":file_cabinet:")

st.header("Invoice Extractor")
input=st.text_input("input prompt:",key="input")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


submit=st.button("Tell me about the invoive")

input_prompt="""
you are an expert in understanding invoices. You will receive input images as invoices and you will have to answer questions based on the input image.
"""

## when submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input, image_data, input_prompt)

    st.subheader("The Response is")
    st.write(response)










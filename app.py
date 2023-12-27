from dotenv import load_dotenv
load_dotenv() # load all environment variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel('gemini-pro-vision')

def get_gemni_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_detail(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Multilanguage Invoice Extractor")
input=st.text_input("Input Prompt:",key="input")
uploaded_file=st.file_uploader("Choose an image.....",type=["jpg","jpeg","png"])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("tell me about the invoice")

input_prompt="""You are an expert in understanding invoice. We will upload an image as invoices and you will have to answer 
any questions based on the uploaded invoices
"""
if submit:
    image_data=input_image_detail(uploaded_file)
    response=get_gemni_response(input_prompt,image_data,input)
    st.subheader("Response")
    st.write(response)


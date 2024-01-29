# importing libraries
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

# Step 1: Confirgure API_KEY

genai.configure(api_key=os.getenv("API_KEY")) # API_KEY is being assigned with our google gemini api key in .env file

# Step 2: create a method to get response from google-pro-vision for the given image and prompt

def get_response(prompt, image):
    """
    this method takes the user given prompt and image and performs the task that user asked on the image and returns a response
    :param prompt: user given prompt
    :param image: user uploaded image
    :return: returns gemini-pro generated response
    """
    model = genai.GenerativeModel('gemini-pro-vision') # using gemini-pro-vision model to work on image data
    response = model.generate_content([prompt, image[0]]) # response holds the response given by the model
    return response.text

def reformat_image(uploaded_image):
    """
    Since, the model gemini-pro-vision takes images as bytes, we need to reformat the image uploaded by
    the user in the form that gemini-pro-vision can understand.
    :param uploaded_image: user uploaded image
    :return: returns the image_data which is a list of dictionary with the type of image and bytes data of user uploaded image
    """
    if uploaded_image is not None:
        # if user uploaded image is not None (valid file)
        image_data = [
            {
                "mime_type": uploaded_image.type, # type of the image uploaded by user
                "data": uploaded_image.getvalue() # bytes data of the image uploaded by user
            }
        ]
        return image_data
    else: # is no image is uploaded, raise error
        raise FileNotFoundError('No file uploaded')

# Step 3:  initialize streamlit page

# page title
st.set_page_config(page_title='Caloriy count')
# page header
st.header('Get calories in your food.')
# file upload option
uploaded_image = st.file_uploader('Upload image', type=['jpg','png', 'jpeg']) # image file types supported are 'jpg','png', 'jpeg'

# display the user uploaded image on the screen
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded image', use_column_width=True)

prompt="""
As an AI with expertise in nutrition, your task is to analyze the food items in the provided image. 
Calculate the total caloric content and provide a detailed breakdown for each item, including its individual caloric intake. 
The format should be as follows:

Food Item 1 - Caloric Value
Food Item 2 - Caloric Value 
Food Item 3 - Caloric Value 
… - …
… - …

Additionally, based on the total caloric content, provide an assessment of whether this meal is suitable for consumption.

If the total calorie content is too high, suggest the best way to consume it like eating a half of it or a quarter of it. 
Also suggest what expercise to do to burn the calories gained like taking 1000 steps, etc.
"""
#submit button for the user
submit = st.button('Calculate Calories')

if submit:
    image_data = reformat_image(uploaded_image) # reformat image (convert the user uploaded image to gemini-pro-vision model understandable format
    response = get_response(prompt, image_data) # give prompt and image to model and get response
    st.header("Response:") # header for response
    st.write(response) # displaying model's response

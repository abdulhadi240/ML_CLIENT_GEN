from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header
import PIL
import google.generativeai as genai
import requests 
from io import BytesIO
from Classes import CheckProfile
import os


api_key = os.getenv('GOOGLE_AI_KEY')
genai.configure(api_key=f'{api_key}')

model = genai.GenerativeModel('gemini-pro-vision')

def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))
    return image



# Function to check profile
def check_profile(image_data: CheckProfile = Body(...)) -> str:
    Profile1 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709453195/3_rarjnr.jpg')
    Profile2 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709453196/2_mj13hg.jpg')
    Profile3 = load_image_from_url(image_data.image_url)
    
    primary_images = [Profile1, Profile2, Profile3]

    # Generate content using the model
    response = model.generate_content([
        "The below primary images are profile pictures of the best creators in the LinkedIn community. These profiles are 9/10",
        primary_images[0], primary_images[1],
        "This is the secondary image. You have to give suggestions and tips on how this profile image can be improved. Also give rating out of 10",
        primary_images[2]
    ])
    return response.text
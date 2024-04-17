import PIL
import google.generativeai as genai
from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests 
from io import BytesIO
from Classes import CheckBanner
import os

api_key = os.getenv('GOOGLE_AI_KEY')
genai.configure(api_key=f'{api_key}')
model = genai.GenerativeModel('gemini-pro-vision')


def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))
    return image


    
    
def check_banner(image_data : CheckBanner = Body(...)) -> str :
    Profile1 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709367740/1704587928601_t90lck.jpg')
    Profile2 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709367740/1708819917247_xur0my.jpg')
    Profile3 = load_image_from_url(image_data.image_url)
    
    primary_images = [Profile1, Profile2, Profile3]

    response = model.generate_content([
        "These are the two banner of most followed influncers in linkedin community . ",
        primary_images[0],
        primary_images[1],
        "individually assess each primary banner, considering factors like design, content quality, and overall attractiveness to viewers. Assign a rating out of 10 to each banner based on its effectiveness in capturing attention and conveying the desired message. Provide actionable tips and suggestions for improving each banner, including adjustments to design elements, content refinement, and other enhancements. Utilize tools such as a generative model to analyze the banners thoroughly and generate detailed insights into their strengths and areas for improvement. Present the analysis and recommendations in a clear and organized manner, possibly using Markdown formatting for readability. Tailor the assessment to align with the banners' overarching goals, whether it's showcasing skills, attracting clients, or promoting a personal brand.",
        "Below is the banner you have to analyze and give suggestions on how to improve it in refernce of the previos banners provided",
        primary_images[2],
        "Only give suggestions, tips, and rating of the  banner. Primary banners are only for taking advice. Dont mention the primary banner . "
    ])

    return response.text     
    


    

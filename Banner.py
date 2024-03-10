import PIL
import google.generativeai as genai
from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests 
from io import BytesIO



GOOGLE_AI_STUDIO = "AIzaSyAK6vhyL_4BvSlHZgY3YjSTVePzU5ZiIUM"
genai.configure(api_key=GOOGLE_AI_STUDIO)
model = genai.GenerativeModel('gemini-pro-vision')

def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))
    return image

class CheckBanner(BaseModel):
    image_url: str | None = None
    
    
def check_banner(image_data : CheckBanner = Body(...)) -> str :
    Profile1 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709367740/1704587928601_t90lck.jpg')
    Profile2 = load_image_from_url('https://res.cloudinary.com/dfkn6xcg4/image/upload/v1709367740/1708819917247_xur0my.jpg')
    Profile3 = load_image_from_url(image_data.image_url)
    
    primary_images = [Profile1, Profile2, Profile3]

    response = model.generate_content([
        "Effectively analyze the primary banners of top creators on LinkedIn and offer comprehensive ratings, tips, suggestions, and content insights, follow these steps. These are the two primary banners",
        primary_images[0],
        primary_images[1],
        "individually assess each primary banner, considering factors like design, content quality, and overall attractiveness to viewers. Assign a rating out of 10 to each banner based on its effectiveness in capturing attention and conveying the desired message. Provide actionable tips and suggestions for improving each banner, including adjustments to design elements, content refinement, and other enhancements. Utilize tools such as a generative model to analyze the banners thoroughly and generate detailed insights into their strengths and areas for improvement. Present the analysis and recommendations in a clear and organized manner, possibly using Markdown formatting for readability. Tailor the assessment to align with the banners' overarching goals, whether it's showcasing skills, attracting clients, or promoting a personal brand.",
        "This is secondary banner",
        primary_images[2],
        "Only give suggestions, tips, and rating of the secondary banner. Primary banners are only for taking advice"
    ])

    return response.text     
    


    

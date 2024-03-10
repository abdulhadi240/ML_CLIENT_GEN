from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import PIL
import google.generativeai as genai
from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests 
from io import BytesIO
from groq import Groq


app : FastAPI = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    

class HeadlineRequest(BaseModel):
    prev_headline: str

def headline_check(feild : str = Query(None) , subfeild : str = Query(None) ,  Prev_headline : HeadlineRequest = Body(...) ) -> str :
    if feild and subfeild :
        client = Groq(api_key='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')
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are an Expert in Writing Headlines for linkedin profile "
                },
                {
                    "role": "user",
                    "content": f"""The user is  {feild} and expert in {subfeild} . His  headline is ***{Prev_headline}*** . !!!You have to improve this headline in a very professional and apealing way and in refernce to the  headline!!! . Dont give anything more just the improved version of the headline"""
                },
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        return(completion.choices[0].message.content)
    else :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "invalid feild")
    


def check_token(xtts_token : str = Header(...)) -> bool :
    if xtts_token == 'Abdulhadi123456789' :
        return True
    else :
        return False

def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))
    return image


class CheckProfile(BaseModel):
    image_url: str | None = None

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

@app.post("/api/headline")
def get_headline(headline: Annotated[str, Depends(headline_check)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : headline}
    else :
        return {'Failed' : 'Invalid Token'} 



@app.post("/api/profile")
def get_profile(profile : Annotated[str, Depends(check_profile)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : profile}
    else :
        return {'Failed' : 'Invalid Token'} 




@app.post("/api/banner")
def check_banner1(banner : Annotated[str, Depends(check_banner)] , authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : banner}
    else :
        return {'Failed' : 'Invalid Token'} 
    


def check_token1(xtts_token : str = Header(...)) -> bool :
    if xtts_token == 'thisisthesecrettoken' :
        return True
    else :
        return False
    
    
    
# @app.post("/api/profile_data")
# def get_data(Data : Annotated[str, Depends(get_profile_data)] , authorization : Annotated[bool , Depends(check_token1)]):
#     if authorization == True :
#         return {'Data' : Data}
#     else :
#         return {'Failed' : 'Invalid Token . To Access this api contact Abdul hadi'} 
            
            
    

    
    
    




    
    
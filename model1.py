import PIL
import google.generativeai as genai
from fastapi import FastAPI, Body
from pydantic import BaseModel
import requests 
from io import BytesIO
from Classes import CheckBanner
import os

api_key = os.getenv('GOOGLE_AI_KEY')
genai.configure(api_key="AIzaSyByQn7n4wEEH-5sPFbFiikkLq2SyXuSOdg")
model = genai.GenerativeModel('gemini-1.0-pro')

    
    
def check_Gem(company_data : str  = Body(...)) -> str :

    response = model.generate_content([
        f"""The data below is a dataset of a company . Use the dataset and predict the company's sales of the next 30 days . Note your are expert in predicting sales
        {company_data}"""
    ])

    return response.text     
    


    

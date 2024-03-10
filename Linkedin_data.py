from linkedin_api import Linkedin
from sqlalchemy import create_engine, text
from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header
from typing import Annotated
from typing import Optional
from pydantic import BaseModel
from groq import Groq

# Authenticate using any Linkedin account credentials
api = Linkedin('ah912425@gmail.com', 'Arq1jas112200!')

def get_profile_data(Profile_Name : str = Body(...)):
    profile = api.get_profile(Profile_Name)
    return profile

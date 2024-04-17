from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from Banner import check_banner
from Authentication import check_token
from Headline import headline_check
from Profile import check_profile
from Resume import check_resume



app : FastAPI = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/banner")
def Analyze_Banner(banner : Annotated[str, Depends(check_banner)] , authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : banner}
    else :
        return {'Failed' : 'Invalid Token'} 
    


@app.post("/api/v1/headline")
def Analyze_Headline(headline: Annotated[str, Depends(headline_check)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : headline}
    else :
        return {'Failed' : 'Invalid Token'} 
    


@app.post("/api/v1/profile")
def Analyze_Profile(profile : Annotated[str, Depends(check_profile)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : profile}
    else :
        return {'Failed' : 'Invalid Token'} 


@app.post("/api/v1/resume")
def Analyze_Resume(resume: Annotated[str , Depends(check_resume)], authorization : Annotated[bool , Depends(check_token)]):
    if authorization == True :
        return {'Data' : resume}
    else :
        return {'Failed' : 'Invalid Token'} 
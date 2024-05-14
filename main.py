from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from model1 import check_Gem
from model2 import Data_Gro
from model3 import check_resume



app : FastAPI = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/XG_Boost")
def XG_Boost(data : Annotated[dict, Depends(check_Gem)]):
    return data


@app.post("/api/v1/LSTM")
def LSTM(data: Annotated[dict, Depends(Data_Gro)]):
   return data
    
    


@app.post("/api/v1/Vector_Auto_Regression")
def VAR(data : Annotated[dict, Depends(check_resume)]):
    return data

@app.post("/")
def Data_Checking():
   return 'api working'
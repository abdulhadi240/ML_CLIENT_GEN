from fastapi import FastAPI, Depends, HTTPException, Query, status , Body , Header


def check_token(xtts_token : str = Header(...)) -> bool :
    if xtts_token == 'Abdulhadi123456789' :
        return True
    else :
        return False
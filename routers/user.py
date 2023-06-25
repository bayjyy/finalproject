from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import userSchema, User
from typing import Optional

user_router = APIRouter()

@user_router.post('/add-user')
def add_user(req:userSchema, db: Session = Depends(get_db)):
    try:
        result =crud.create_crud(req, User, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

@user_router.get('/get-user')
def get_user(
    department_id: Optional[int] = None,
    position_id: Optional[int] = None,
    db: Session = Depends(get_db)):
    try:
        result = crud.read_users(department_id, position_id, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@user_router.put('/update-user/{id}')
def update_user(id: int, req: userSchema, db: Session = Depends(get_db)):
    try:
        result = crud.update_user(id, req, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    

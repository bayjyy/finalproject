from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import positionSchema, Position
from typing import Optional

position_router = APIRouter()

@position_router.post('/add-position')
def add_position(req:positionSchema, db: Session = Depends(get_db)):
    try:
        result =crud.create_crud(req, Position, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

@position_router.get('/get-position')
def get_position(
    department_id: Optional[int] = None,
    db: Session = Depends(get_db)):
    try:
        result =crud.read_position(department_id, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@position_router.put('/update-position/{id}')
def update_position(id: int, req: positionSchema, db: Session = Depends(get_db)):
    try:
        result = crud.update_position(id, req, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

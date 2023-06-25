from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import itemSchema, Item

item_router = APIRouter()

@item_router.post('/add-item')
def add_item(req:itemSchema, db: Session = Depends(get_db)):
    try:
        result =crud.create_crud(req, Item, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

@item_router.get('/get-item')
def get_item(db: Session = Depends(get_db)):
    try:
        result =crud.read_item(db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@item_router.put('/update-item/{id}')
def update_item(id: int, req: itemSchema, db: Session = Depends(get_db)):
    try:
        result = crud.update_item(id, req, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')

from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import responsesSchema, Responses
from typing import Optional

responses_router = APIRouter()

@responses_router.post('/responses', dependencies=[Depends(HTTPBearer())])
def add_responses(req:responsesSchema, header_param: Request, db: Session = Depends(get_db)):
    try:
        result = crud.create_responses(req, header_param, db)
        if result:
            return JSONResponse(status_code=status.HTTP_201_CREATED, 
                content={'result': 'Successfully added to responses'})
        else:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                content={'result': 'This user not found'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
    
@responses_router.get('/responses', dependencies=[Depends(HTTPBearer())])
def add_responses(header_param: Request, requests_id: int, db: Session = Depends(get_db)):
    try:
        result = crud.read_responses(header_param, requests_id, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
        elif result == False:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                content={'result': 'This user not found'})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'NO CONTENT'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@responses_router.put('/update-responses/{id}', dependencies=[Depends(HTTPBearer())])
def update_responses(id: int, req: responsesSchema, header_param: Request,  db: Session = Depends(get_db)):
    try:
        result = crud.update_responses(id, req, header_param, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
        elif result == False:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                content={'result': 'This user not found'})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'NO CONTENT'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')


from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import requestsSchema, Requests
from typing import Optional

requests_router = APIRouter()

@requests_router.post('/add-requests/', dependencies=[Depends(HTTPBearer())])
def add_requests(req:requestsSchema, header_param: Request, db: Session = Depends(get_db)):
    try:
        result = crud.create_requests(req, header_param, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={'result': 'Successfully added to requests'})
        else:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={'result': 'This user not found'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@requests_router.get('/requests', dependencies=[Depends(HTTPBearer())])
def add_requests(header_param: Request, req_status: Optional[bool] = None, db: Session = Depends(get_db)):
    try:
        result = crud.read_requests(header_param, req_status, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
        elif result == False:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={'result': 'This user not found'})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'NO CONTENT'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')    


@requests_router.put('/update-requests/{id}', dependencies=[Depends(HTTPBearer())])
def update_requests(id: int, req: requestsSchema, header_param: Request, db: Session = Depends(get_db)):
    try:
        result = crud.update_requests(id, req, header_param, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
        elif result == False:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={'result':'This user not found'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
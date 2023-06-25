from fastapi import *
from fastapi. requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud
from models import registerSchema, loginSchema, userSchema

authentication_router = APIRouter()

@authentication_router.post('/sign-in',dependencies=[Depends(HTTPBearer())])
def sign_in(req: loginSchema, header_param: Request, db: Session= Depends(get_db)):
    try:
        result = crud.signIn(req, header_param, db)
        if result:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={'result': 'Successfully added to signIn'})
        else:
            return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={'result': 'This user not found'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    

@authentication_router.get('/user/', dependencies=[Depends(HTTPBearer())])
def get_user(department_id, position_id, header_param: Request, db: Session = Depends(get_db)):
    try:
        result = crud.read_user(department_id, position_id, header_param, db)
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


@authentication_router.post('/new-user/',dependencies=[Depends(HTTPBearer())])
def new_user(req: userSchema, header_param:Request, db: Session = Depends(get_db)):
    try:
        result = crud.create_new_user(req, header_param, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'result': 'User already exists'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"result": 'Something went wrong'})
    
@authentication_router.put('/delete-user/{id}',dependencies=[Depends(HTTPBearer())])
def delete_user(id:int, header_param:Request, db: Session = Depends(get_db)):
    try:
        result = crud.delete_user(id, header_param, db)
        if result:
            result = jsonable_encoder(result)
            return JSONResponse(status_code = status.HTTP_200_OK, content=result)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'result': 'User already exists'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Something went wrong')
     

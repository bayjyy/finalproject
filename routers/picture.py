from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import *
from sqlalchemy.orm import *
from db import get_db
import crud

picture_router = APIRouter()

@picture_router.post('/upload-picture')
def picture_image(id: int, db:Session=Depends(get_db),file: UploadFile = File(...)):
    try:
        result = crud.create_img(id,file,db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code = status.HTTP_201_CREATED,content=result)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong')
    
@picture_router.delete('/delete-picture{id}')
def delete_picture(id: int, db: Session = Depends(get_db)):
    try:
        result = crud.delete_img(id, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"result": "DELETED"})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"result": "NO DELETED"})   
    
    
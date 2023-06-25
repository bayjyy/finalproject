from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import Base, engine
from routers import *

app = FastAPI()

Base.metadata.create_all(engine)
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')

app.include_router(item_router, tags=['Item'])
app.include_router(picture_router, tags=['Picture'])
app.include_router(user_router, tags=['User'])
app.include_router(department_router, tags=['Department'])
app.include_router(position_router, tags=['Position'])
app.include_router(responses_router, tags=['Responses'])
app.include_router(requests_router, tags=['Requests'])
app.include_router(authentication_router, tags=['Authentication'])

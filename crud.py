from sqlalchemy.orm import *
from sqlalchemy import *
from fastapi import *
from db import get_db
from sqlalchemy import or_, and_
from upload_depends import upload_image, delete_uploaded_image 
from token import create_access_token, decode_token, check_token
from models import *
import sys
import os

def create_crud(req, model, db:Session):
    new_add = model(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add

def read_item(db: Session):
    result = db.query(Item).options(joinedload(Item.picture)).first()
    return result

def update_item(id: int, req: itemSchema, db: Session = Depends(get_db)):
    new_update = db.query(Item).filter(Item.id == id)\
        .update({
            Item.title              : req.title,
            Item.quantity           : req.quantity,
            Item.price              : req.price,
            Item.material_number    : req.material_number,
            Item.vendor             : req.vendor,
            Item.order              : req.order,
            Item.bin_location       : req.bin_location
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Successfully update"
    else:
        return False
    
def read_department(db: Session):
    result = db.query(Department).all()
    return result
    
def update_department(id: int, req: departmentSchema, db: Session = Depends(get_db)):
    new_update = db.query(Department).filter(Department.id == id)\
        .update({
            Department.name       : req.name
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Successfully update"
    else:
        return False
    
def read_position(department_id, db:Session):
    result = db.query(
        Position)\
    
    if department_id:
        result = result.filter(Position.department_id == department_id)
    result = result.all()
    return result 

def update_position(id: int, req: positionSchema, db: Session = Depends(get_db)):
    new_update = db.query(Position).filter(Position.id == id)\
        .update({
            Position.name       : req.name
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Successfully update"
    else:
        return False
    
def read_users(department_id, position_id, db):
    result = db.query(
        User)\
        
    if department_id:
        result = result.filter(User.department_id == department_id)
    if position_id:
        result = result.filter(User.position_id == position_id)
    result = result.all()
    return result
    
def update_user(id: int, req: userSchema, db: Session = Depends(get_db)):
    new_update = db.query(User).filter(User.id == id)\
        .update({
            User.name       : req.name,
            User.staff_id   : req.staff_id,
            User.type       : req.type
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Successfully update"
    else:
        return False
    
def create_responses(req, header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    new_add = Responses(
        user_id = user.id,
        requests_id = req.requests_id,
        status = req.status,
        description = req.description
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add

def read_responses(header_param, requests_id, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    result = db.query(
        Responses
    )\
    .options(joinedload(Responses.user).load_only('user_name'))\
    .join(Requests,Requests.id == Responses.requests_id)
    if requests_id:
            result = result.filter(Responses.requests_id == requests_id)
    return result.all()

def update_responses(id, req, header_param, db:Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    new_update = db.query(Responses).filter(Responses.id == id)\
        .update({
            Responses.status            : req.status,
            Responses.description       : req.description
        }, synchronize_session=False)\
        
    db.commit()
    if new_update:
        return "Successfully update"
    else:
        return False

def create_requests(req, header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    new_add = Requests(
        user_id = user.id,
        department_id = user.department_id,
        position_id = user.position_id,
        item_id = req.item_id,
        req_quantity = req.req_quantity,
        req_date = req.req_date
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def read_requests(header_param, req_status, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    result = db.query(
        Requests
    )\
        .options(joinedload(Requests.item))\
            .options(joinedload(Requests.user).load_only('user_name'))
    
    if req_status == True:
        result = result.filter(Requests.status == True)
    elif req_status == False:
        result = result.filter(Requests.status == False)
    return result.all()

def update_requests(id, req, header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    new_update = db.query(Requests).filter(Requests.id == id)\
        .update({
            Requests.req_quantity   : req.req_quantity,
            Requests.req_date       : req.req_date
        }, synchronize_session=False)\
        
    db.commit()
    if new_update:
        return "Successfully update"
    else:
        return False
    
def create_response(req, db: Session):
    db.query(Requests).filter(Requests.id == req.requests_id)\
        .update(
            {
                Requests.status: True
            }, 
            synchronize_session=False
        )
    db.commit()
    new_add = Responses(**req.dict())
    db.add(new_add)
    db.commit()

    
def create_img(id, file, db:Session):
    uploaded_file_name=upload_image('item', file)
    new_add = Picture(
        img =uploaded_file_name,
        item_id = id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add

def delete_img(id, db:Session):
    image = db.query(Picture).filter(Picture.id ==id).first()
    if image.img:
        delete_uploaded_image(image_name=image.img)
        db.query(Picture).filter(Picture.id == id)\
            .delete(synchronize_session=False)
        db.commit()
    return True


def create_new_user(req, header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    user = db.query(User).filter(User.user_name == req.user_name).first()
    if user:
        return False
    payload = {
        'user_name': req.user_name,
        'password': req.password
    }
    token = create_access_token(payload)
    new_add = User(
        user_name = req.user_name,
        password = req.password,
        staff_id = req.staff_id,
        token = token,
        type = req.type,
        department_id = req.department_id,
        position_id = req.position_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add

def signIn(req, header_param, db):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    user = db.query(User.token).filter(
        and_(
            User.user_name == req.user_name,
            User.password == req.password
        )
    ).first()
    if user:
        return user
    db.commit()

    
def read_user(department_id, position_id, header_param, db):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    result = db.query(
        User)\
        
    if department_id:
        result = result.filter(User.department_id == department_id)
    if position_id:
        result = result.filter(User.position_id == position_id)
    result = result.all()
    return result
    

def delete_user(id, header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    user_name: str = payload.get('user_name')
    password: str = payload.get('password')
    user = read_user_id(user_name, password, db)
    if not user:
        return False
    new_delete = (db.query(User).filter(User.id == id).delete(synchronize_session=False))
    db.commit()
    if new_delete:
        return 'SUCCESFULLY DELETED'
    else:
        return "NO DELETED" 

def read_user_id(user_name, password, db: Session):
    user = db.query(User.id, User.department_id, User.position_id)\
        .filter(and_(User.user_name == user_name, User.password == password))\
            .first()
    if user:
        return user
    
from sqlalchemy import *
from sqlalchemy.orm import *
from db import Base
from datetime import *

class Item(Base):
    __tablename__ = 'item'
    id              = Column(Integer, primary_key=True, index=True)
    title           = Column(String)
    quantity        = Column(Integer)
    price           = Column(Float)
    material_number = Column(String)
    order           = Column(Integer)
    vendor          = Column(String)
    bin_location    = Column(String)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    picture         = relationship('Picture', back_populates='item')
    requests        = relationship('Requests', back_populates='item')


class Picture(Base):
    __tablename__ = 'picture'
    id              = Column (Integer, primary_key=True, index=True)
    img             = Column (String)
    item_id         = Column(Integer, ForeignKey('item.id'))
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    item            = relationship('Item', back_populates='picture')
    

class User(Base):
    __tablename__ = 'user'
    id              = Column(Integer, primary_key=True, index=True)
    user_name       = Column(String)
    password        = Column(String)
    token           = Column(String)
    staff_id        = Column(String)
    type            = Column(String)
    is_deleted      = Column(Boolean, default=False)
    department_id   = Column(Integer, ForeignKey('department.id'))
    position_id     = Column(Integer, ForeignKey('position.id'))
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    requests        = relationship('Requests', back_populates='user')
    department      = relationship('Department', back_populates='user')
    position        = relationship('Position', back_populates='user')
    responses       = relationship('Responses', back_populates='user')

    
 
class Department(Base):
    __tablename__ ='department'
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String)     
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    position        = relationship('Position', back_populates='department')
    user            = relationship('User', back_populates='department')
    requests        = relationship('Requests', back_populates='department')
    
    
class Position(Base):
    __tablename__ = "position"
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String)
    department_id   = Column(Integer, ForeignKey('department.id'))
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    department      = relationship('Department', back_populates='position')
    user            = relationship('User', back_populates='position')
    requests        = relationship('Requests', back_populates='position')
    

class Responses(Base):
    __tablename__ = 'responses'
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey('user.id'))
    requests_id     = Column(Integer, ForeignKey('requests.id'))
    status          = Column(Boolean, default=False)
    description     = Column(String)
    
    requests        = relationship('Requests', back_populates='responses')
    user            = relationship('User', back_populates='responses')
    

class Requests(Base):
    __tablename__ = 'requests'
    id              = Column(Integer, primary_key=True, index=True)
    item_id         = Column(Integer, ForeignKey('item.id'))
    department_id   = Column(Integer, ForeignKey('department.id'))
    position_id     = Column(Integer, ForeignKey('position.id'))
    user_id         = Column(Integer, ForeignKey('user.id'))
    req_quantity    = Column(Integer)
    req_date        = Column(String)
    status          = Column(Boolean, default=False)
    create_at       = Column(DateTime, default=datetime.now)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    item            = relationship('Item', back_populates='requests')
    user            = relationship('User', back_populates='requests')
    department      = relationship('Department', back_populates='requests')
    position        = relationship('Position', back_populates='requests')
    responses       = relationship('Responses', back_populates='requests')
    



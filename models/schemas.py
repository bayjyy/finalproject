from pydantic import BaseModel

class itemSchema(BaseModel):
    title           : str
    quantity        : int        
    price           : float         
    material_number : str 
    order           : int           
    vendor          : str          
    bin_location    : str 

class userSchema(BaseModel):
    user_name       : str
    password        : str
    staff_id        : str
    type            : str
    department_id   : int
    position_id     : int
    

class departmentSchema(BaseModel):
    name            : str

class positionSchema(BaseModel):
    name: str
    department_id   : int
    
    
class responsesSchema(BaseModel):
    status          : bool
    description     : str
    requests_id     : int

class requestsSchema(BaseModel):
    item_id         : int         
    req_quantity    : int
    req_date        : str

class loginSchema(BaseModel):
    user_name       : str
    password        : str
    
class registerSchema(loginSchema):
    user_name       : str
    retype_password : str
    
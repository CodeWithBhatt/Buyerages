from pydantic import BaseModel
from typing import List

# <<<--------Authorization-------->>>
class Add_Account(BaseModel):
    name : str
    usn : str
    email : str
    sex : str
    phone : str
    password : str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str
    user : str
    class Config():
        orm_mode = True

class UserData(BaseModel):
    username : str
    user : str

# <<<--------Seller/Renter-------->>>
class OwnerProperty(BaseModel):
    name : str
    number : str
    description : str
    location : str
    pincode : str
    for_sell : bool
    for_rent : bool
    price : int
    rent : int
    status : bool
    class Config():
        orm_mode = True

class Owner(BaseModel):
    name : str
    usn : str
    email : str
    phone : str
    property : List[OwnerProperty]
    class Config():
        orm_mode = True

class AddProperty(BaseModel):
    name : str
    number : str
    description : str
    location : str
    pincode : str
    for_sell : bool = False
    for_rent : bool = False
    price : int
    rent : int
    class Config():
        orm_mode = True

# <<<--------Buyer-------->>>
class PropertyToBuy(BaseModel):
    name : str
    number : str
    owner : str
    description : str
    location : str
    pincode : str
    price : int
    class Config():
        orm_mode = True

class BuyPropertyForm(BaseModel):
    number : str
    owner : str
    price : int
    taxes : float
    total_price : float
    class Config():
        orm_mode = True

class SubmitBuyProperty(BuyPropertyForm):
    token : float
    class Config():
        orm_mode = True

# <<<--------Renter-------->>>
class PropertyToRent(BaseModel):
    name : str
    number : str
    owner : str
    description : str
    location : str
    pincode : str
    rent : int
    class Config():
        orm_mode = True

class RentPropertyForm(BaseModel):
    number : str
    owner : str
    rent : int
    downpayment: float
    class Config():
        orm_mode = True

class SubmitRentProperty(RentPropertyForm):
    tenure:  int
    class Config():
        orm_mode = True

# <<<--------Renter-------->>>
class BuyProperty(BaseModel):
    name : str
    number : str
    description : str
    location : str
    pincode : str
    price : int
    status : bool
    class Config():
        orm_mode = True

class RentProperty(BaseModel):
    name : str
    number : str
    description : str
    location : str
    pincode : str
    rent : int
    status : bool
    class Config():
        orm_mode = True

class BuyPropertyRecord(BaseModel):
    id : int
    property : str
    owner : str
    customer : str
    price : int
    tax : float
    total : float
    token : float
    purchase : str
    verify : bool
    class Config():
        orm_mode = True

class RentPropertyRecord(BaseModel):
    id : int
    property : str
    owner : str
    customer : str
    rent : int
    downpayment : float
    tenure : int
    booking : str
    verify : bool
    class Config():
        orm_mode = True

class contact(BaseModel):
    name : str
    address : str
    email : str
    number : str
    subject: str
    desc : str
    class Config():
        orm_mode = True
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Rent, Authenticate as Auth
from typing import List

router = APIRouter( prefix='/rent', tags=['Rent'])
templates = Jinja2Templates(directory="View/User")
db = database.get_db


@router.get("/", response_class=HTMLResponse, response_model=List[Schema.PropertyToRent], status_code=status.HTTP_200_OK)
def property(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    properties = Rent.All_Property(db)
    # return properties # remove response_class from decorator
    return templates.TemplateResponse("RentProperty.html", {"request":request, "data":properties})

@router.get("/rentproperty", response_class=HTMLResponse, response_model=Schema.RentPropertyForm, status_code=status.HTTP_200_OK)
def rent_property(request:Request, property_number:str, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    result = Rent.Extract_PropertyData(property_number, current_user.username, db)
    # return result # remove response_class from decorator
    return templates.TemplateResponse("RentPropertyForm.html", {"request":request, "data":result})

@router.post("/rentproperty", status_code=status.HTTP_201_CREATED)
def submit_purchase(request:Schema.SubmitRentProperty, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    result = Rent.Submit_Purchase(request, current_user.username, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unable to register')
    return {"status":"Successful", "data":result}
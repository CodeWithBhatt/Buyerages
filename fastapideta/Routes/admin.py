from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Admin, Authenticate as Auth
from typing import List, Dict

router = APIRouter( prefix='/admin', tags=['admin'])
templates = Jinja2Templates(directory="View/Admin")
db = database.get_db

@router.get('/', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def Admin_Dashboard(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user)):
    if current_user.user == 'admin':
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admin can access this")

@router.get('/property', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def All_Property(request:Request, current_user:Schema.UserData = Depends(Auth.get_current_user), db : Session = Depends(db)):
    if current_user.user == 'admin':
        property = Admin.All_Property(db)
        return templates.TemplateResponse("property.html", {"request": request, "data": property})
        # return {"data":property} # remove response_class from decorator
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admin can access this")

@router.put('/property', status_code=status.HTTP_202_ACCEPTED)
def verify_property(number:str, current_user:Schema.UserData = Depends(Auth.get_current_user), db : Session = Depends(db)):
    if current_user.user == 'admin':
        property = Admin.Verify_Property(number, db)
        return property
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admin can access this")

@router.get('/record', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def All_Record(request:Request, current_user:Schema.UserData = Depends(Auth.get_current_user), db : Session = Depends(db)):
    if current_user.user == 'admin':
        record = Admin.All_Record(db)
        result = {"BuyRecord":record[0], "RentRecord":record[1]}
        # return {"data":result} # remove response_class from decorator
        return templates.TemplateResponse("record.html", {"request":Request, "data":result})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admin can access this")

@router.put('/record', status_code=status.HTTP_202_ACCEPTED)
def verify_record(type:str, id:int, current_user:Schema.UserData = Depends(Auth.get_current_user), db : Session = Depends(db)):
    if current_user.user == 'admin':
        record = Admin.Verify_Record(type, id, db)
        return record
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admin can access this")
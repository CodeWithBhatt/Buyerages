from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Sell, Authenticate as Auth

router = APIRouter( prefix='/sell', tags=['Sell'])
templates = Jinja2Templates(directory="View/User")
db = database.get_db

@router.get("/", status_code=status.HTTP_200_OK)
async def redirect_to_property(current_user:Schema.UserData = Depends(Auth.get_current_user), db : Session = Depends(db)):
    return RedirectResponse("/sell/property")

@router.get("/property", response_class=HTMLResponse, response_model=Schema.Owner, status_code=status.HTTP_200_OK)
def property(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    all_property = Sell.Get_Property(current_user.username, db)
    # return all_property # remove response_class from decorator
    return templates.TemplateResponse("sellproperty.html", {"request":request, "data":all_property})

@router.get("/addproperty", response_class=HTMLResponse, response_model=Schema.Owner, status_code=status.HTTP_200_OK)
def property(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    return templates.TemplateResponse("addproperty.html", {"request":request})

@router.post("/addproperty", status_code=status.HTTP_201_CREATED)
def add_property(request:Schema.AddProperty, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    new_property = Sell.AddProperty(request, current_user.username, db)
    if not new_property:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Invalid Data")
    else:
        return new_property

@router.delete("/property", status_code=status.HTTP_202_ACCEPTED)
def delete_property(property_number:str, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    delete_property = Sell.DeleteProperty(property_number,current_user.username, db)
    if not delete_property:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Property details couldn't be found")
    return delete_property
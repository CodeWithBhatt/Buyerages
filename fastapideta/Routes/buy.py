from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import database
from sqlalchemy.orm import Session
from Backend import Schema, Buy, Authenticate as Auth
from typing import List

router = APIRouter( prefix='/buy', tags=['Buy'])
templates = Jinja2Templates(directory="View/User")
db = database.get_db


@router.get("/", response_class=HTMLResponse, response_model=List[Schema.PropertyToBuy], status_code=status.HTTP_200_OK)
def property(request:Request, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    properties = Buy.All_Property(db)
    # return properties # remove response_class from decorator
    return templates.TemplateResponse("BuyProperty.html", {"request":request, "data":properties})

@router.post("/buyproperty", status_code=status.HTTP_201_CREATED)
def submit_purchase(request:Schema.SubmitBuyProperty, current_user:Schema.UserData=Depends(Auth.get_current_user), db:Session=Depends(db)):
    result = Buy.Submit_Purchase(request, current_user.username, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unable to register')
    return {"status":"Successful", "data":result}
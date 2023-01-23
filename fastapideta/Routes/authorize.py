from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Database import model, database
from Backend import Schema, Authenticate as Auth
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])
templates = Jinja2Templates(directory="Views")
db = database.get_db

@router.get('/signup', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def load_signup_page(request:Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_account(request:Schema.Add_Account, db : Session = Depends(db)):
    user = Auth.Find_User(request, db)
    if not user:
        new_user = Auth.Add_User(request, db)
        if type(new_user)==model.User:
            return RedirectResponse(url="/home")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Account was not created")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account with USN {request.usn} already registered")

@router.get('/login', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def load_login_page(request:Request):
    return templates.TemplateResponse("login.html", {'request': request})

@router.post('/login', response_model=Schema.Token, status_code=status.HTTP_200_OK)
async def user_login(request:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(db)):
    access_token = Auth.Login(request, db)
    return access_token
    
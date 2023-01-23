from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from Database import model, database as db
from Routes import admin, sell, buy, rent, authorize as auth

model.db.Base.metadata.create_all(db.engine)
template = Jinja2Templates(directory='View')
app = FastAPI(
    title="Buyerages",
    description="18CSL58 DBMS Laboratory Mini Project on Property Management",
    version="2.1.0",
    swagger_ui_oauth2_redirect_url='/login',
    contact={
        "Developer 1": {
            "Name" : "Jayapradha B",
            "USN"  : "1HK20CS059",
            "Mail" : "1hk20cs059@hkbk.edu.in",
            "Role" : "Backend Engineer"
        },
        "Developer 2": {
            "Name" : "Farman Ali",
            "USN"  : "1HK20CS046",
            "Mail" : "1hk20cs046@hkbk.edu.in",
            "Role" : "Frontend Engineer"
        },
        "Developer 2": {
            "Name" : "Anurag Bhatt",
            "USN"  : "1HK20CS028",
            "Mail" : "1hk20cs028@hkbk.edu.in",
            "Role" : "Web Administrator"
        }
    }
)

app.include_router(admin.router)
app.include_router(sell.router)
app.include_router(buy.router)
app.include_router(rent.router)
app.include_router(auth.router)

@app.get('/home', status_code=status.HTTP_200_OK)
async def redirect_to_home():
    return RedirectResponse('/')

@app.get('/', response_class=HTMLResponse, status_code=status.HTTP_200_OK, tags=['Home'])
async def home(data:Request):
    return template.TemplateResponse("home.html", {"request":data})

@app.get('/about', response_class=HTMLResponse, status_code=status.HTTP_200_OK, tags=['Home'])
async def about(data:Request):
    return template.TemplateResponse("about.html", {"request":data})

@app.get('/contact', response_class=HTMLResponse, status_code=status.HTTP_200_OK, tags=['Home'])
async def contact(data:Request):
    return template.TemplateResponse("contact.html", {"request":data})
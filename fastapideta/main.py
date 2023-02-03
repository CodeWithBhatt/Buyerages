from fastapi import Depends, FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from Database import model, database as db
from Routes import admin, sell, buy, rent, authorize as auth
from Backend import Schema
from sqlalchemy.orm import Session

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

@app.get('/service', response_class=HTMLResponse, status_code=status.HTTP_200_OK, tags=['Home'])
async def service(data:Request):
    return template.TemplateResponse("service.html", {"request":data})

@app.post('/submit-contact')
def submit(request:Schema.contact, db:Session = Depends(db.get_db)):
    detail = model.Contact(name=request.name, address=request.address, email=request.email, number=request.number, subject=request.subject, desc=request.desc)
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail
from operator import and_
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import Schema
from Database import model
from datetime import datetime

def All_Property(db:Session):
    property = db.query(model.Property).filter(and_(model.Property.status == True, model.Property.rent == True)).all()
    result = [Schema.PropertyToRent(name = p.name, number = p.number, owner=p.owner, description=p.desc, location=p.location, pincode=p.pincode, rent=p.rent_price) for p in property]
    return result

def Extract_PropertyData(property:str, username:str, db:Session):
    propertydata = db.query(model.Property).filter(and_(model.Property.status == True, model.Property.number == property, model.Property.rent == True)).first()
    result = Schema.RentPropertyForm(number=property, owner = propertydata.owner, customer=username, rent=propertydata.rent_price, downpayment=(0.3*property.rent_price))
    return result

def Submit_Purchase(data:Schema.SubmitRentProperty, username:str, db:Session):
    if username == data.customer:
        try:
            new_record = model.RentRecord(property=data.number, owner=data.owner, customer=data.customer, rent = data.rent, downpayment=data.downpayment, tenure=data.tenure, bookingdate=datetime.today().strftime('%Y-%m-%d'), verification = 'False')
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return new_record
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Unable to register due to issue: {e}')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please register from same id from which you selected the property')
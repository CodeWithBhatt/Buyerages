from operator import and_
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import Schema
from Database import model

def Get_Property(username:str, db:Session):
    owner_property = db.query(model.Property).filter(model.Property.owner == username).all()
    property_list = [Schema.OwnerProperty(name=p.name, number=p.number, description=p.desc, location=p.location, pincode=p.pincode, for_sell=p.sell, for_rent=p.rent, price=p.sell_price, rent=p.rent_price, status=p.status) for p in owner_property]
    owner_detail = db.query(model.User).filter(model.User.usn == username).first()
    result = Schema.Owner(name=owner_detail.name, usn=owner_detail.usn, email=owner_detail.email, phone=owner_detail.phone, property=property_list)
    return result

def AddProperty(data:Schema.AddProperty, username:str, db:Session):
    find_property = db.query(model.Property).filter(model.Property.number == data.number).first()
    if not find_property:
        try:
            new_property = model.Property(name=data.name, number=data.number, desc=data.description, location=data.location, pincode=data.pincode, owner=username, sell=data.for_sell, rent=data.for_rent, sell_price=data.price, rent_price=data.rent, status=False)
            db.add(new_property)
            db.commit()
            db.refresh(new_property)
            return new_property
        except Exception as e:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Property details not added due to following error {e}")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Property number {data.number} is already registered with us")

def DeleteProperty(data:str, currentuser:str, db:Session):
    try:
        property = db.query(model.Property).filter(and_(model.Property.number == data, model.Property.owner == currentuser))
        if not property.first():
            return None
        property.delete(synchronize_session=False)
        db.commit()
        return {"data": data, "status":"Deleted"}
    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Property details not deleted due to following error {e}")
    
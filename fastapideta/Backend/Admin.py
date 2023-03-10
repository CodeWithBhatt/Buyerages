from operator import and_
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import Schema
from Database import model
from typing import List

def All_Property(db : Session):
    properties = db.query(model.Property).all()
    buy = [Schema.BuyProperty(name=p.name, number=p.number, description=p.desc, location=p.location, pincode=p.pincode, price=p.sell_price, status=p.status) for p in properties if p.sell == True]
    rent = [Schema.RentProperty(name=p.name, number=p.number, description=p.desc, location=p.location, pincode=p.pincode, rent=p.rent_price, status=p.status) for p in properties if p.rent == True]
    result = {"BuyProperty":buy, "RentProperty":rent}
    return result

def Verify_Property(num:str, db:Session):
    query = db.query(model.Property).filter(model.Property.number == num)
    query.update({model.Property.status : (not (query.first().status))})
    db.commit()
    return {"data":"Sucessfull"}

def All_Record(db : Session):
    buy_records = db.query(model.BuyRecord).all()
    rent_records = db.query(model.RentRecord).all()
    buy = [Schema.BuyPropertyRecord(id=b.record_id, property=b.property, owner=b.owner, customer=b.customer, price=b.price, tax=b.tax, total=b.total, token=b.token, purchase=str(b.purchasedate), verify=b.verification) for b in buy_records]
    rent = [Schema.RentPropertyRecord(id=r.record_id, property=r.property, owner=r.owner, customer=r.customer, rent=r.rent, downpayment=r.downpayment, tenure=r.tenure, booking=str(r.bookingdate), verify=r.verification) for r in rent_records]
    return {"BuyRecord":buy, "RentRecord":rent}

def Verify_Record(type:str, id: int, db:Session):
    if type=='buy':
        query = db.query(model.BuyRecord).filter(model.BuyRecord.record_id == id)
        query.update({model.BuyRecord.verification : True})
        db.commit()
        query1 = db.query(model.BuyRecord).filter(model.BuyRecord.record_id == id).first()
        query2 = db.query(model.Property).filter(model.Property.number == query1.property)
        query2.update({model.Property.owner : query.first().customer, model.Property.status : False})
        db.commit()
        return {"status": "success", "data":"buy record updated"}
    if type=='rent':
        query = db.query(model.RentRecord).filter(model.RentRecord.record_id == id)
        query.update({model.RentRecord.verification : True})
        db.commit()
        query1 = db.query(model.RentRecord).filter(model.RentRecord.record_id == id).first()
        query2 = db.query(model.Property).filter(model.Property.number == query1.property)
        query2.update({model.Property.status : False})
        db.commit()
        return {"status": "success", "data":"rent record updated"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid type")
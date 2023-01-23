from operator import and_
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import Schema
from Database import model

def All_Property(db : Session):
    properties = db.query(model.Property).all()
    buy = [Schema.BuyProperty(name=p.name, number=p.number, description=p.desc, location=p.location, pincode=p.pincode, price=p.sell_price, status=p.status) for p in properties if p.sell == True]
    rent = [Schema.RentProperty(name=p.name, number=p.number, description=p.desc, location=p.location, pincode=p.pincode, rent=p.rent_price, status=p.status) for p in properties if p.rent == True]
    return (buy, rent)

def All_Record(db : Session):
    buy_records = db.query(model.BuyRecord).all()
    rent_records = db.query(model.RentRecord).all()
    buy = [Schema.BuyProperty(id=b.record_id, property=b.property, owner=b.owner, customer=b.customer, price=b.price, tax=b.tax, total=b.total, token=b.token, purchase=str(b.purchasedate), verify=b.verification) for b in buy_records]
    rent = [Schema.RentProperty(id=r.record_id, property=r.property, owner=r.owner, customer=r.customer, rent=r.rent, downpayment=r.downpayment, tenure=r.tenure, booking=str(r.bookingdate), verify=r.verification) for r in rent_records]
    return (buy, rent)

def Verify_Record(type:str, id: int, db:Session):
    if type=='buy':
        query = db.query(model.BuyRecord).filter(model.BuyRecord.record_id == id)
        query.update({model.BuyRecord.verification : True})
        db.commit()
        return {"status": "success", "data":"buy record updated"}
    if type=='rent':
        query = db.query(model.RentRecord).filter(model.RentRecord.record_id == id)
        query.update({model.RentRecord.verification : True})
        db.commit()
        return {"status": "success", "data":"rent record updated"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid type")
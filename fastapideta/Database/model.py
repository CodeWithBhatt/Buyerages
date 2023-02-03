from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Float
from sqlalchemy.orm import relationship
from . import database as db

class User(db.Base):
    __tablename__ = 'user'
    name = Column(String(50), nullable=False)
    usn = Column(String(10), primary_key=True, nullable=False)
    email = Column(String(50), primary_key=True, nullable=False)
    sex = Column(String(2), nullable=False)
    phone = Column(String(13), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(10), nullable=False, default='user')

class Property(db.Base):
    __tablename__ = 'property'
    name = Column(String(30), nullable=False)
    number = Column(String(20), primary_key=True, nullable=False)
    desc = Column(String(500), nullable=False)
    location = Column(String(50), nullable=False)
    pincode = Column(String(8), nullable=False)
    owner = Column(String(10), ForeignKey('user.usn'), nullable=False)
    sell = Column(Boolean, nullable=False, default=False)
    rent = Column(Boolean, nullable=False, default=False)
    sell_price = Column(Integer)
    rent_price = Column(Integer)
    status = Column(Boolean, nullable=False, default=False)
    USER = relationship("User")
    BUYRECORD = relationship('BuyRecord', cascade="all, delete-orphan")
    RENTRECORD = relationship('RentRecord', cascade="all, delete-orphan")

class BuyRecord(db.Base):
    __tablename__ = 'buy_record'
    record_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    property = Column(String(20), ForeignKey('property.number', ondelete='CASCADE'), primary_key=True, nullable=False)
    owner = Column(String(10), ForeignKey('user.usn'), nullable=False)
    customer = Column(String(10), ForeignKey('user.usn'), nullable=False)
    price = Column(Integer, nullable=False)
    tax = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    token = Column(Float, nullable=False)
    purchasedate = Column(Date, nullable=False)
    verification = Column(Boolean, nullable=False, default=False)
    USER = relationship("User",foreign_keys=[owner])
    USER1 = relationship("User",foreign_keys=[customer])
    PROPERTY = relationship("Property", overlaps="BUYRECORD")

class RentRecord(db.Base):
    __tablename__ = 'rent_record'
    record_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    property = Column(String(20), ForeignKey('property.number', ondelete='CASCADE'), primary_key=True, nullable=False)
    owner = Column(String(10), ForeignKey('user.usn'), nullable=False)
    customer = Column(String(10), ForeignKey('user.usn'), nullable=False)
    rent = Column(Integer, nullable=False)
    downpayment = Column(Float, nullable=False)
    tenure = Column(Integer, nullable=False)
    bookingdate = Column(Date, nullable=False)
    verification = Column(Boolean, nullable=False, default=False)
    USER = relationship("User", foreign_keys=[owner])
    USER1 = relationship("User", foreign_keys=[customer])
    PROPERTY = relationship("Property", overlaps="RENTRECORD")

class Contact(db.Base):
    __tablename__ = "contact"
    contact_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50))
    address = Column(String(200))
    email = Column(String(50))
    number = Column(String(15))
    subject = Column(String(100))
    desc = Column(String(500))
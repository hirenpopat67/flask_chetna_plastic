from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from flask_login import UserMixin

class Customers(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.Text)
    customer_place = db.Column(db.Text)
    mobile_no = db.Column(db.Integer)
    discount_percentage = db.Column(db.Integer)
    gst_no = db.Column(db.Text)
    date_time_added = db.Column(db.DateTime, default=datetime.utcnow)

class Products(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Text)
    product_price = db.Column(db.Text)
    date_time_added = db.Column(db.DateTime, default=datetime.utcnow)


class Invoices(db.Model):

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.Integer,unique=True)
    customer_name = db.Column(db.Text)
    customer_place = db.Column(db.Text)
    invoice_date  = db.Column(db.Date)
    invoice_json = db.Column(db.Text)
    date_time_added = db.Column(db.DateTime, default=datetime.now())

class Users(UserMixin,db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    google_account_json = db.Column(db.Text)
    logged_in = db.Column(db.Boolean, default=False)
    last_logged_in =  db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

class Company(db.Model):

    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.Text)
    company_gst_no = db.Column(db.Text)
    company_logo = db.Column(db.LargeBinary)
    company_favicon = db.Column(db.LargeBinary)
    date_time_added = db.Column(db.DateTime, default=datetime.now())
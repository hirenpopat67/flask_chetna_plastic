from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from flask_login import UserMixin

class Customers(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.Text)
    customer_place = db.Column(db.Text)
    mobile_no = db.Column(db.Text)
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
    company_logo = db.Column(db.Text)
    company_favicon = db.Column(db.Text)
    date_time_added = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def ensure_dummy_data(cls):
        # Check if any company records exist
        existing_company = cls.query.first()
        if not existing_company:
            # No records found, insert dummy data

            try:
                with open('../static/images/dummy_logo_base64.txt', 'r') as f:
                    dummy_img = f.read()
            except FileNotFoundError:
                pass
                # Handle the error (e.g., log it, raise an exception, etc.)
            except Exception as e:
                pass
                # Handle other possible exceptions
                
            dummy_company = cls(
                company_name="Dummy Company",
                company_gst_no="DUMMY123456",
                company_logo=dummy_img,
                company_favicon=dummy_img,
                date_time_added=datetime.now()
            )
            db.session.add(dummy_company)
            db.session.commit()
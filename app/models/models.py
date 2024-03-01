from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

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
    invoice_date  = db.Column(db.DateTime)
    invoice_product_details = db.Column(db.Text)
    sub_total_amount = db.Column(db.Text)
    discount_percentage = db.Column(db.Text)
    discount_amount = db.Column(db.Text)
    total_amount = db.Column(db.Text)
    gst_amount = db.Column(db.Text)
    final_bill_amount = db.Column(db.Text)
    date_time_added = db.Column(db.DateTime, default=datetime.now())

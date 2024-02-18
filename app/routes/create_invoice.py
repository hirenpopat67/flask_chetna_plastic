from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices,Customers,Products
from datetime import datetime

create_invoice_blueprint = Blueprint('create_invoice_blueprint', __name__)


@create_invoice_blueprint.route('/create_invoice')
def create_invoice():
    try:

        all_customers = Customers.query.order_by(Customers.customer_name).all()

        fetch_invoice_no = Invoices.query.order_by(Invoices.invoice_no.desc()).first()

        if fetch_invoice_no:
            fetch_last_invoice_no = fetch_invoice_no.invoice_no + 1
        else:
            fetch_last_invoice_no = 1

        today_invoice_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

        all_products = Products.query.order_by(Products.product_name).all()

        context = {

        'all_customers': all_customers,
        'fetch_last_invoice_no': fetch_last_invoice_no,
        'today_invoice_date': today_invoice_date,
        'all_products': all_products,

    }
        
        return render_template('create_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices,Customers,Products
from datetime import datetime

create_invoice_blueprint = Blueprint('create_invoice_blueprint', __name__)


@create_invoice_blueprint.route('/create_invoice',methods = ['GET','POST'])
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
        
        if request.method == 'POST':
            print("request:- ",request)
            invoice_data = request.form.to_dict()
            customer_name = invoice_data.setdefault('customer_name')
            customer_mobile_no = invoice_data.setdefault('customer_mobile_no')
            customer_place = invoice_data.setdefault('customer_place')
            customer_gst_no = invoice_data.setdefault('customer_gst_no')
            parcel_details = invoice_data.setdefault('parcel_details')
            total_parcel = invoice_data.setdefault('total_parcel')
            total_parcel = invoice_data.setdefault('total_parcel')
            invoice_number = invoice_data.setdefault('invoice_number')
            invoice_date = invoice_data.setdefault('invoice_date')

            if not invoice_number:
                fetch_invoice_no = Invoices.query.order_by(Invoices.invoice_no.desc()).first()

                if fetch_invoice_no:
                    invoice_number = invoice_number.invoice_no
                else:
                    invoice_number = 1

            format_invoice_date = datetime.strptime(invoice_date, '%Y-%m-%d')
            # print("invoice_data:- ",invoice_data)

            
        
        return render_template('create_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
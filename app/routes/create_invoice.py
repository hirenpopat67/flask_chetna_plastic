from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Invoices,Customers,Products
from datetime import datetime,date
from app import db
import json

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
            invoice_data = request.form.to_dict()
            customer_name = invoice_data.setdefault('customer_name')
            customer_place = invoice_data.setdefault('customer_place')
            invoice_number = invoice_data.setdefault('invoice_number')
            invoice_date = invoice_data.setdefault('invoice_date')
            sub_total_amount = invoice_data.setdefault('sub_total_amount')
            discount_percentage = invoice_data.setdefault('discount_percentage')
            discount_amount = invoice_data.setdefault('discount_amount')
            total_amount = invoice_data.setdefault('total_amount')
            gst_amount = invoice_data.setdefault('gst_amount')
            final_amount = invoice_data.setdefault('final_amount')

            if not invoice_number:
                fetch_invoice_no = Invoices.query.order_by(Invoices.invoice_no.desc()).first()

                if fetch_invoice_no:
                    invoice_number = fetch_invoice_no.invoice_no + 1
                else:
                    invoice_number = 1
            
            if invoice_date:
                print(invoice_date)

                invoice_date_obj = datetime.strptime(invoice_date, '%Y-%m-%d')
                formatted_invoice_date = invoice_date_obj.strftime('%d-%m-%Y')

            else:
                formatted_invoice_date = date.today().strftime('%d-%m-%Y')
            
            
            add_new_invoice_data = Invoices(
                invoice_no = invoice_number,
                customer_name = customer_name,
                customer_place = customer_place,
                invoice_date = formatted_invoice_date,
                invoice_product_details = json.dumps(invoice_data),
                sub_total_amount = sub_total_amount,
                discount_percentage = discount_percentage,
                discount_amount = discount_amount,
                total_amount = total_amount,
                gst_amount = gst_amount,
                final_bill_amount = final_amount,
            )

            db.session.add(add_new_invoice_data)

            try:
                db.session.commit()
                flash("Invoice successfully added",'success')
                return redirect('/create_invoice')
            except Exception as e:
                flash(e,'danger')
                return redirect('500.html'), 500

            
        
        return render_template('create_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
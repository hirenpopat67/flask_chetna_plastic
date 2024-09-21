from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Invoices,Customers,Products
from datetime import datetime,date
from app import db
import json
from flask_login import login_required

add_invoice_blueprint = Blueprint('add_invoice_blueprint', __name__)


@add_invoice_blueprint.route('/add_invoice',methods = ['GET','POST'])
@login_required
def add_invoice():
    try:

        action = request.form.get('action',None)

        all_customers = Customers.query.order_by(Customers.customer_name).all()

        fetch_invoice_no = Invoices.query.order_by(Invoices.invoice_no.desc()).first()

        if fetch_invoice_no:
            default_invoice_number = fetch_invoice_no.invoice_no + 1
        else:
            default_invoice_number = 1

        default_invoice_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

        all_products = Products.query.order_by(Products.product_name).all()

        context = {

        'all_customers': all_customers,
        'default_invoice_number': default_invoice_number,
        'default_invoice_date': default_invoice_date,
        'all_products': all_products,

    }
        
        if request.method == 'POST':
            invoice_data = request.form.to_dict(flat=False)
            validation_error = invoice_data_validator(invoice_data)
            if validation_error:
                flash(validation_error,'error')
                return redirect('/add_invoice')
            
            invoice_data_processed = invoice_data_processor(invoice_data)
            
             # save invoice
            

            invoice_data_processed_json = json.dumps(invoice_data_processed)
            add_new_invoice_data = Invoices(
                invoice_no = invoice_data['invoice_number'][0],
                customer_name = invoice_data['customer_name'][0],
                customer_place = invoice_data['customer_place'][0],
                invoice_date = datetime.strptime(invoice_data['invoice_date'][0], '%Y-%m-%d'),
                invoice_json = invoice_data_processed_json
            )

            db.session.add(add_new_invoice_data)

            try:
                db.session.commit()
                flash(f"{invoice_data['customer_name'][0]} Customer Invoice successfully added",'success')

                if action == "save_and_print":
                    return redirect(f'/view_invoice?id={add_new_invoice_data.id}')


                return redirect('add_invoice')
            except Exception as e:
                flash(e,'danger')
                return redirect('500.html'), 500

            
        return render_template('add_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


def invoice_data_validator(invoice_data):
    # Validate Invoice Info ----------

    # invoice-number
    try:
        invoice_number = int(invoice_data['invoice_number'][0])
    except:
        print("Error: Incorrect Invoice Number")
        return "Error: Incorrect Invoice Number"
    
    # invoice date
    try:
        date_text = invoice_data['invoice_date'][0]
        datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Error: Incorrect Invoice Date")
        return "Error: Incorrect Invoice Date"

    # customer-name
    if len(invoice_data['customer_name'][0]) < 1:
        print("Error: Incorrect Customer Name")
        return "Error: Incorrect Customer Name"

    return None


def invoice_data_processor(invoice_data):

    processed_invoice_data = {}


    # Convert ImmutableMultiDict to a list of dictionaries

    processed_invoice_data['customer_name'] = invoice_data['customer_name'][0]
    processed_invoice_data['customer_place'] = invoice_data['customer_place'][0]
    processed_invoice_data['customer_mobile_no'] = invoice_data['customer_mobile_no'][0]
    processed_invoice_data['customer_gst_no'] = invoice_data['customer_gst_no'][0]
    processed_invoice_data['parcel_details'] = invoice_data['parcel_details'][0]
    processed_invoice_data['note'] = invoice_data['note'][0]
    processed_invoice_data['invoice_number'] = invoice_data['invoice_number'][0]
    processed_invoice_data['invoice_date'] = invoice_data['invoice_date'][0]

    processed_invoice_data['items'] = []
    
    for idx, product in enumerate(invoice_data['product_name']):
        if product:
            item_entry = {}
            item_entry['product_name'] = product
            item_entry['qty'] = invoice_data['qty'][idx]
            item_entry['product_price'] = invoice_data['product_price'][idx]
            item_entry['total_price_amount'] = invoice_data['total_price_amount'][idx]

            processed_invoice_data['items'].append(item_entry)


    processed_invoice_data['sub_total_amount'] = invoice_data['sub_total_amount'][0]
    processed_invoice_data['discount_percentage'] = invoice_data['discount_percentage'][0]
    processed_invoice_data['discount_amount'] = invoice_data['discount_amount'][0]
    processed_invoice_data['total_amount'] = invoice_data['total_amount'][0]
    processed_invoice_data['gst_amount'] = invoice_data['gst_amount'][0]
    processed_invoice_data['final_amount'] = invoice_data['final_amount'][0]

    # print(processed_invoice_data)
    return processed_invoice_data


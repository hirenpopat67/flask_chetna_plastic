from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices,Customers,Products
import json
from app.routes.create_invoice import invoice_data_validator,invoice_data_processor
from datetime import datetime
from app import db
from flask_login import login_required

edit_invoice_blueprint = Blueprint('edit_invoice_blueprint', __name__)


@edit_invoice_blueprint.route('/edit_invoice',methods=['GET','POST'])
@login_required
def edit_invoice():
    try:
        data = {}

        id = request.args.get('id',None)


        fetch_invoice = Invoices.query.order_by(Invoices.id == id)

        for fi in fetch_invoice:
            for column in fi.__table__.columns:

                column_value = (getattr(fi, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value
            
            data['invoice_json'] = json.loads(fi.invoice_json)

        all_customers = Customers.query.order_by(Customers.customer_name).all()

        all_products = Products.query.order_by(Products.product_name).all()

        context = {

        'data': data,
        'all_customers': all_customers,
        'all_products': all_products,

    }
        
        if request.method == 'POST':
            invoice_data = request.form.to_dict(flat=False)
            validation_error = invoice_data_validator(invoice_data)
            if validation_error:
                flash(validation_error,'error')
                return redirect('/all_invoice')
            
            invoice_data_processed = invoice_data_processor(invoice_data)
            
             # save invoice
            
            invoice_data_processed_json = json.dumps(invoice_data_processed)

            invoice_no = invoice_data['invoice_number'][0]

            update_invoice_data = Invoices.query.filter(Invoices.invoice_no == invoice_no).first()

            if update_invoice_data:

                print("invoice_data:-",invoice_data)

                update_invoice_data.customer_name = invoice_data['customer_name'][0]
                update_invoice_data.customer_place = invoice_data['customer_place'][0]
                update_invoice_data.invoice_date = datetime.strptime(invoice_data['invoice_date'][0], '%Y-%m-%d')
                update_invoice_data.invoice_json = invoice_data_processed_json


                try:
                    db.session.commit()
                    flash("Invoice successfully updated",'success')
                    return redirect('all_invoices')
                except Exception as e:
                    flash(e,'danger')
                    return redirect('500.html'), 500
        
        return render_template('edit_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
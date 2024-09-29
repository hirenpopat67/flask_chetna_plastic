from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices,Customers,Products
import json
from app.routes.add_invoice import invoice_data_validator,invoice_data_processor
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

        fetch_invoice = Invoices.query.filter(Invoices.id == id).first()

        if request.method == 'POST':
            action = request.form.get('action',None)
            invoice_data = request.form.to_dict(flat=False)
            validation_error = invoice_data_validator(invoice_data)
            if validation_error:
                flash(validation_error,'error')
                return redirect('/all_invoices')
            
            invoice_data_processed = invoice_data_processor(invoice_data)
            
            # save invoice

            try:
                include_gst_checkbox = invoice_data['include_gst_checkbox'][0]
                is_gst = True
            except:
                    invoice_data_processed.update({'gst_amount':'0.00','final_amount':invoice_data_processed['total_amount']})
                    is_gst = False
            
            invoice_data_processed_json = json.dumps(invoice_data_processed)

            if fetch_invoice:

                fetch_invoice.customer_name = invoice_data['customer_name'][0]
                fetch_invoice.customer_place = invoice_data['customer_place'][0]
                fetch_invoice.invoice_date = datetime.strptime(invoice_data['invoice_date'][0], '%Y-%m-%d')
                fetch_invoice.invoice_json = invoice_data_processed_json
                fetch_invoice.is_gst = is_gst

                try:
                    db.session.commit()
                    flash(f"{invoice_data['customer_name'][0]} Customer Invoice successfully updated",'success')

                    if action == "update_and_print":
                        return redirect(f'/view_invoice?id={fetch_invoice.id}')

                    return redirect('all_invoices')
                except Exception as e:
                    flash(e,'danger')
                    return redirect('500.html'), 500
            else:
                flash('Invoice not found','error')
                return redirect('/all_invoices')

        else:
    
            for column in fetch_invoice.__table__.columns:

                column_value = (getattr(fetch_invoice, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value
            
                data['invoice_json'] = json.loads(fetch_invoice.invoice_json)

            all_customers = Customers.query.order_by(Customers.customer_name).all()

            all_products = Products.query.order_by(Products.product_name).all()

            context = {

            'data': data,
            'all_customers': all_customers,
            'all_products': all_products,

            }
            
            return render_template('edit_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
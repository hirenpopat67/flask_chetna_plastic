from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices,Customers
from datetime import datetime

add_invoice_blueprint = Blueprint('add_invoice_blueprint', __name__)


@add_invoice_blueprint.route('/add_invoice')
def add_invoice():
    try:

        all_customers = Customers.query.order_by(Customers.customer_name).all()

        fetch_invoice_no = Invoices.query.order_by(Invoices.invoice_no.desc()).first()

        if fetch_invoice_no:
            fetch_last_invoice_no = fetch_invoice_no.invoice_no + 1
        else:
            fetch_last_invoice_no = 1

        today_invoice_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

        context = {

        'all_customers': all_customers,
        'fetch_last_invoice_no': fetch_last_invoice_no,
        'today_invoice_date': today_invoice_date,

    }
        
        return render_template('add_invoice.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
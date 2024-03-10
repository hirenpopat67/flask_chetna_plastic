from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices
import json

edit_invoice_blueprint = Blueprint('edit_invoice_blueprint', __name__)


@edit_invoice_blueprint.route('/edit_invoice/<int:id>')
def edit_invoice(id):
    try:
        data = {}

        fetch_invoice = Invoices.query.order_by(Invoices.id == id)

        for fi in fetch_invoice:
            for column in fi.__table__.columns:

                column_value = (getattr(fi, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value
            
            data['invoice_json'] = json.loads(fi.invoice_json)
        
        return render_template('edit_invoice.html',data=data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
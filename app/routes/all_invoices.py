from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices

all_invoices_blueprint = Blueprint('all_invoices_blueprint', __name__)


@all_invoices_blueprint.route('/all_invoices')
def all_invoices():
    try:
        data = []

        fetch_all_invoices = Invoices.query.order_by(Invoices.invoice_no.desc()).all()

        for fai in fetch_all_invoices:
            new_data = {}
            for column in fai.__table__.columns:

                column_value = (getattr(fai, column.name))

                if not column_value:
                    column_value = ''

                new_data[column.name] = column_value
                

            data.append(new_data)
        
        return render_template('all_invoices.html',data=data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
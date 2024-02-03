from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Invoices
from app import db

delete_invoice_blueprint = Blueprint('delete_invoice_blueprint', __name__)


@delete_invoice_blueprint.route('/delete_invoice',methods=['POST'])
def delete_invoice():
    try:

        id = request.form.get('delete_invoice_id')
        
        if id:
            delete_inv = Invoices.query.filter(Invoices.id == id).first()

            if delete_inv:
                db.session.delete(delete_inv)
                db.session.commit()

                flash('Invoice successfully deleted','success')
                return redirect(url_for('all_invoices_blueprint.all_invoices'))
            
        flash('Please provide apprpriate Invoice','warning')
        return render_template('all_invoices.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
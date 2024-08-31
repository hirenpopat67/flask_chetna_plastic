from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Customers
from app import db
from flask_login import login_required

delete_customer_blueprint = Blueprint('delete_customer_blueprint', __name__)


@delete_customer_blueprint.route('/delete_customer',methods=['GET'])
@login_required
def delete_customer():
    try:
        id = request.args.get('delete_customer_id')
        
        if id:
            delete_cus = Customers.query.filter(Customers.id == id).first()

            if delete_cus:
                db.session.delete(delete_cus)
                db.session.commit()

                flash(f'{delete_cus.customer_name} Customer successfully deleted','error')
                return redirect(url_for('all_customers_blueprint.all_customers'))
            
        flash('Please provide apprpriate Customer','warning')
        return render_template('all_customers.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
from flask import Blueprint,render_template,redirect,current_app,request,flash,jsonify
from app.models.models import Customers
from flask_login import login_required

get_single_customer_blueprint = Blueprint('get_single_customer_blueprint', __name__)


@get_single_customer_blueprint.route('/get_single_customer/<string:customer_name>')
@login_required
def get_single_customer(customer_name):
    try:
        data = {}

        filter_cus = Customers.query.filter(Customers.customer_name == customer_name).first()

        if filter_cus:
            for column in filter_cus.__table__.columns:

                column_value = (getattr(filter_cus, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value

        
        return jsonify(data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
from flask import Blueprint,render_template,redirect,current_app,request,flash,jsonify
from app.models.models import Customers

get_single_customer_from_id_blueprint = Blueprint('get_single_customer_from_id_blueprint', __name__)


@get_single_customer_from_id_blueprint.route('/get_single_customer_from_id/<string:id>')
def get_single_customer_from_id(id):
    try:
        data = {}

        filter_cus = Customers.query.filter(Customers.id == id).first()

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
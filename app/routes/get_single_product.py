from flask import Blueprint,render_template,redirect,current_app,request,flash,jsonify
from app.models.models import Products
from flask_login import login_required

get_single_product_blueprint = Blueprint('get_single_product_blueprint', __name__)


@get_single_product_blueprint.route('/get_single_product/<string:product_name>')
@login_required
def get_single_product(product_name):
    try:
        data = {}

        filter_pro = Products.query.filter(Products.product_name == product_name).first()

        if filter_pro:
            for column in filter_pro.__table__.columns:

                column_value = (getattr(filter_pro, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value

        
        return jsonify(data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
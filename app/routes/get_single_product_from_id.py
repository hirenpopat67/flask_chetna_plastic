from flask import Blueprint,render_template,redirect,current_app,request,flash,jsonify
from app.models.models import Products

get_single_product_from_id_blueprint = Blueprint('get_single_product_from_id_blueprint', __name__)


@get_single_product_from_id_blueprint.route('/get_single_product_from_id/<string:id>')
def get_single_product_from_id(id):
    try:
        data = {}

        filter_pro = Products.query.filter(Products.id == id).first()

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
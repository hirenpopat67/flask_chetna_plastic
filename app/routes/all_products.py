from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Products

all_products_blueprint = Blueprint('all_products_blueprint', __name__)


@all_products_blueprint.route('/all_products')
def all_products():
    try:
        data = []

        fetch_all_products = Products.query.order_by(Products.product_name.asc()).all()

        for fap in fetch_all_products:
            new_data = {}
            for column in fap.__table__.columns:

                column_value = (getattr(fap, column.name))

                if not column_value:
                    column_value = ''

                new_data[column.name] = column_value
                

            data.append(new_data)
        
        return render_template('all_products.html',data=data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
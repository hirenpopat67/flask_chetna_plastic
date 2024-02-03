from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Customers

all_customers_blueprint = Blueprint('all_customers_blueprint', __name__)


@all_customers_blueprint.route('/all_customers')
def all_customers():
    try:
        data = []

        fetch_all_customers = Customers.query.order_by(Customers.customer_name.asc()).all()

        for fac in fetch_all_customers:
            new_data = {}
            for column in fac.__table__.columns:

                column_value = (getattr(fac, column.name))

                if not column_value:
                    column_value = ''

                new_data[column.name] = column_value
                

            data.append(new_data)
        
        return render_template('all_customers.html',data=data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
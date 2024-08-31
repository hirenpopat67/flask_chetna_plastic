from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Customers
import json
from app import db
from flask_login import login_required

edit_customer_blueprint = Blueprint('edit_customer_blueprint', __name__)


@edit_customer_blueprint.route('/edit_customer',methods=['GET','POST'])
@login_required
def edit_customer():
    try:
        data = {}

        id = request.args.get('id',None)


        fetch_customer = Customers.query.filter(Customers.id == id).first()
        

        if request.method == 'POST':
            customer_name = request.form.get('customer_name',None)
            customer_place = request.form.get('customer_place',None)
            customer_mobile_no = request.form.get('customer_mobile_no',None)
            customer_gst_no = request.form.get('customer_gst_no',None)
            customer_discount_percentage = request.form.get('customer_discount_percentage',None)

            if not customer_name or not customer_place:
                flash('Customer Name and Customer Place cannot empty','error')
                return redirect('/edit_customer')


            fetch_customer.customer_name = customer_name,
            fetch_customer.customer_place = customer_place,
            fetch_customer.mobile_no = customer_mobile_no,
            fetch_customer.gst_no = customer_gst_no,
            fetch_customer.discount_percentage = customer_discount_percentage

            db.session.commit()
            
            flash(f'{customer_name} Customer successfully updated','success')
            return redirect('/all_customers')
        else:
            for column in fetch_customer.__table__.columns:

                column_value = (getattr(fetch_customer, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value

            return render_template('edit_customer.html',data=data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
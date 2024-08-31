from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Customers
from datetime import datetime,date
from app import db
import json
from flask_login import login_required

add_customer_blueprint = Blueprint('add_customer_blueprint', __name__)


@add_customer_blueprint.route('/add_customer',methods = ['GET','POST'])
@login_required
def create_customer():
    try:
        if request.method == 'POST':
            customer_name = request.form.get('customer_name',None)
            customer_place = request.form.get('customer_place',None)
            customer_mobile_no = request.form.get('customer_mobile_no',None)
            customer_gst_no = request.form.get('customer_gst_no',None)
            customer_discount_percentage = request.form.get('customer_discount_percentage',None)

            if not customer_name or not customer_place:
                flash('Customer Name and Customer Place cannot empty','error')
                return redirect('/add_customer')

            check_exist_cus = Customers.query.filter(Customers.customer_name == customer_name,Customers.customer_place==customer_place).first()

            if check_exist_cus:
                flash('Customer Name and Customer Place already exist','warning')
                return redirect('/add_customer')


            add_customer = Customers(
                customer_name = customer_name,
                customer_place = customer_place,
                mobile_no = customer_mobile_no,
                gst_no = customer_gst_no,
                discount_percentage = customer_discount_percentage
            )

            db.session.add(add_customer)
            db.session.commit()
            
            flash(f'{customer_name} Customer successfully added','success')
            return redirect('/all_customers')

        return render_template('add_customer.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


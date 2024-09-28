from flask import Blueprint,redirect,current_app,request,flash,jsonify
from app.models.models import Products,Customers
from flask_login import login_required
import pandas as pd
import numpy as np
from app import db

helpers_blueprint = Blueprint('helpers_blueprint', __name__)


@helpers_blueprint.route('/excel_sheet_to_products',methods=['POST'])
@login_required
def excel_sheet_to_products():
    try:
        xls = pd.ExcelFile("2024CP.xlsx")
        sheet_name = "Price List"
        check_dt = pd.read_excel(xls, sheet_name)

        list_of_columns = check_dt.columns.tolist()

        dtype_dict = {}
        for c in list_of_columns:
            dtype_dict[c] = str

        sheet = pd.read_excel(xls, sheet_name, dtype=dtype_dict)

        data = sheet.replace({np.nan: None})

        for values in zip(*[data.loc[0:181, column] for column in list_of_columns]):
            id, product_name,product_price,c = values

            add_product_data = Products(
                product_name=product_name,
                product_price=product_price,
            )

            db.session.add(add_product_data)
        # db.session.commit()

        return jsonify({'success': 'Successfully Transferred'})

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


@helpers_blueprint.route('/excel_sheet_to_customers',methods=['POST'])
@login_required
def excel_sheet_to_customers():
    try:
        xls = pd.ExcelFile("2024CP.xlsx")
        sheet_name = "Customers"
        check_dt = pd.read_excel(xls, sheet_name)

        list_of_columns = check_dt.columns.tolist()

        dtype_dict = {}
        for c in list_of_columns:
            dtype_dict[c] = str


        sheet = pd.read_excel(xls, sheet_name, dtype=dtype_dict)

        data = sheet.replace({np.nan: None})

        for values in zip(*[data.loc[0:425, column] for column in list_of_columns]):
            print('values: ',values)
            id, customer_name,customer_place,gst_1,_,gst_2,_,gst_no,mobile_no = values
            if mobile_no == " ":
                mobile_no = None
            discount_percentage = 45

            add_customer_data = Customers(
                customer_name = customer_name,
                customer_place = customer_place,
                mobile_no = mobile_no,
                discount_percentage = discount_percentage,
                gst_no = gst_no,
            )

            db.session.add(add_customer_data)
        # db.session.commit()

        return jsonify({'success': 'Successfully Transferred'})

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
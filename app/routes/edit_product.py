from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Products
from app import db
from flask_login import login_required

edit_product_blueprint = Blueprint('edit_product_blueprint', __name__)


@edit_product_blueprint.route('/edit_product',methods = ['GET','POST'])
@login_required
def edit_product():
    try:

        data = {}

        id = request.args.get('id',None)

        fetch_product = Products.query.filter(Products.id == id).first()

        if request.method == 'POST':
            product_name = request.form.get('product_name',None)
            product_price = request.form.get('product_price',None)

            if not product_name or not product_price:
                flash('Product Name and Product Price cannot empty','error')
                return redirect('/edit_product')

            check_exist_product = Products.query.filter(Products.product_name == product_name,Products.product_price==product_price).first()

            if check_exist_product:
                flash('Product Name and Product Price already exist','warning')
                return redirect('/edit_product')


            fetch_product.product_name = product_name
            fetch_product.product_price = product_price

            db.session.commit()
            
            flash(f'{product_name} Product successfully updated','success')
            return redirect('/all_products')
        else:
            for column in fetch_product.__table__.columns:

                column_value = (getattr(fetch_product, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value

            return render_template('edit_product.html',data=data)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


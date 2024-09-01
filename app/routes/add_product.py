from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Products
from app import db
from flask_login import login_required

add_product_blueprint = Blueprint('add_product_blueprint', __name__)


@add_product_blueprint.route('/add_product',methods = ['GET','POST'])
@login_required
def add_product():
    try:
        if request.method == 'POST':
            product_name = request.form.get('product_name',None)
            product_price = request.form.get('product_price',None)

            if not product_name or not product_price:
                flash('Product Name and Product Price cannot empty','error')
                return redirect('/add_product')

            check_exist_product = Products.query.filter(Products.product_name == product_name,Products.product_price==product_price).first()

            if check_exist_product:
                flash('Product Name and Product Price already exist','warning')
                return redirect('/add_product')


            add_product = Products(
                product_name = product_name,
                product_price = product_price,
            )

            db.session.add(add_product)
            db.session.commit()
            
            flash(f'{product_name} Product successfully added','success')
            return redirect('/all_products')

        return render_template('add_product.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


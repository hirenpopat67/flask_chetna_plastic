from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from app.models.models import Products
from app import db
from flask_login import login_required

delete_product_blueprint = Blueprint('delete_product_blueprint', __name__)


@delete_product_blueprint.route('/delete_product',methods=['POST'])
@login_required
def delete_product():
    try:
        id = request.form.get('delete_product_id')
        
        if id:
            delete_pro = Products.query.filter(Products.id == id).first()

            if delete_pro:
                db.session.delete(delete_pro)
                db.session.commit()

                flash('Product successfully deleted','success')
                return redirect(url_for('all_products_blueprint.all_products'))
            
        flash('Please provide apprpriate Product','warning')
        return render_template('all_products.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
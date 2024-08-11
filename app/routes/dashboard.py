from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices
import json
from flask_login import login_required

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)


@dashboard_blueprint.route('/dashboard')
# @login_required
def dashboard():
    try:
        return render_template('dashboard.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
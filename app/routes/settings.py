from flask import Blueprint,render_template,redirect,current_app,request,flash
from flask_login import login_required
from app.models.models import Users,Company

settings_blueprint = Blueprint('settings_blueprint', __name__)


@settings_blueprint.route('/settings')
@login_required
def settings():
    try:
        fetch_company_details = Company.query.first()

        return render_template('settings.html',fetch_company_details=fetch_company_details)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
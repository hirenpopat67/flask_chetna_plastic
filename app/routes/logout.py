from flask import Blueprint,render_template,redirect,current_app,request,flash
from flask_login import login_required, logout_user

logout_blueprint = Blueprint('logout_blueprint', __name__)


@logout_blueprint.route('/logout')
@login_required
def logout():
    try:

        logout_user()
        flash('LOGOUT SUCCESSFUL','success')

        return redirect('/')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
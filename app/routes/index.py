from flask import Blueprint,render_template,redirect,current_app,request,flash
from app import db

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index():
    try:

        # db.create_all()

        return render_template('index.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
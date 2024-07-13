from flask import Blueprint,render_template

errorhandler_blueprint = Blueprint('errorhandler_blueprint', __name__)


@errorhandler_blueprint.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
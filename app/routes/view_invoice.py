from flask import Blueprint,render_template,redirect,current_app,request,flash,jsonify
from flask_login import login_required
import pdfkit

view_invoice_blueprint = Blueprint('view_invoice_blueprint', __name__)


@view_invoice_blueprint.route('/view_invoice')
# @login_required
def view_invoice():
    try:
        options = {
            'page-size': 'A4',
        }

        configuration = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

        css = 'css.css'
       
        pdfkit.from_file('test.html', 'out.pdf',options=options,configuration=configuration,css=css)
        return render_template('view_invoice.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
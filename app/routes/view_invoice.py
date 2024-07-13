from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from flask_login import login_required
import pdfkit
import platform
from app.models.models import Invoices 
import json

view_invoice_blueprint = Blueprint('view_invoice_blueprint', __name__)


@view_invoice_blueprint.route('/view_invoice')
# @login_required
def view_invoice():
    try:
        # options = {
        #     'page-size': 'A4',
        # }

        # if platform.system() == 'Windows':
        #     configuration = pdfkit.configuration(
        #         wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

        # elif platform.system() == 'Linux':
        #     configuration = pdfkit.configuration(
        #         wkhtmltopdf='/usr/bin/wkhtmltopdf')

        # else:
        #     current_app.logger.warning('Unknown operating system detected for wkhtmltopdf')
        #     flash('Unknown operating system detected for wkhtmltopdf','error')
        #     return redirect('500.html'), 500
       
        # pdfkit.from_file('app/templates/view_invoice.html', 'out.pdf',options=options,configuration=configuration)

        data = {}

        id = request.args.get('id',None)


        fetch_invoice = Invoices.query.filter(Invoices.id == id).first()

        if fetch_invoice:
        
            for column in fetch_invoice.__table__.columns:

                column_value = (getattr(fetch_invoice, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value
            
            data['invoice_json'] = json.loads(fetch_invoice.invoice_json)
            invoice_date = fetch_invoice.invoice_date
            data['invoice_date'] = f"{invoice_date.day}/{invoice_date.month}/{invoice_date.year}"

            context = {

            'data': data,

            }
            return render_template('view_invoice.html',context=context)
        else:
            return render_template("404.html")

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
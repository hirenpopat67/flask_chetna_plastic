from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for
from flask_login import login_required
import pdfkit
import platform
from app.models.models import Invoices,Company
import json
from base64 import b64encode
from jinja2 import Template


view_invoice_blueprint = Blueprint('view_invoice_blueprint', __name__)


@view_invoice_blueprint.route('/view_invoice')
# @login_required
def view_invoice():
    try:
        options = {
            'page-size': 'A4',
            "enable-local-file-access": ""
        }
       
        configuration = pdfkit.configuration(
            wkhtmltopdf='/usr/bin/wkhtmltopdf')

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


            fetch_company_details = Company.query.first()

            if fetch_company_details:

                logo_base64 =  fetch_company_details.company_favicon
            else:
                logo_base64 = None

            data['logo_base64'] = logo_base64

            context = {

            'data': data,
            'fetch_company_details': fetch_company_details,

            }
            # Step 1: Read the HTML string from the file
            with open('app/templates/view_invoice.html', 'r') as file:
                html_string = file.read()

            # Render the template with data
            template = Template(html_string)

            html_out = template.render(context=context)
            # pdfkit.from_string(html_string, 'out.pdf',options=options,configuration=configuration,css=css)
            pdf_binary = pdfkit.from_string(html_out, False,options=options,configuration=configuration)

            output_pdf_base64 = b64encode(pdf_binary).decode('utf-8')

            return render_template('view_invoice.html',context=context)
        else:
            return render_template("404.html")

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
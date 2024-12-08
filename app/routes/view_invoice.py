from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for,send_file
from flask_login import login_required
import pdfkit
import platform
from app.models.models import Invoices,Company,Customers
import json
from base64 import b64encode
from jinja2 import Template
import io
from app import db,fetch_value_or_none


view_invoice_blueprint = Blueprint('view_invoice_blueprint', __name__)


@view_invoice_blueprint.route('/view_invoice')
@login_required
def view_invoice():
    try:

        data = {}
        id = request.args.get('id',None)
        download_id = request.args.get('download_id',None)

        if download_id:
            id = download_id

        options = {
            'page-size': 'A4',
            "enable-local-file-access": ""
        }
       
        configuration = pdfkit.configuration(
            wkhtmltopdf='/usr/bin/wkhtmltopdf')

        fetch_invoice = (
            db.session.query(Invoices,Customers)
            .filter(Invoices.id == id)
            .join(Customers, Invoices.customer_id == Customers.id)
            .first()
        )

        if fetch_invoice:

            i,c = fetch_invoice
        
            for column in i.__table__.columns:

                column_value = (getattr(i, column.name))

                if not column_value:
                    column_value = ''

                data[column.name] = column_value
            
            data['invoice_json'] = json.loads(i.invoice_json)
            invoice_date = i.invoice_date
            data['invoice_date'] = f"{invoice_date.day}/{invoice_date.month}/{invoice_date.year}"

            # Fetching customer details

            data['customer_id'] = fetch_value_or_none(c,'id',default="")
            data['customer_name'] = fetch_value_or_none(c,'customer_name',default="")
            data['customer_place'] = fetch_value_or_none(c,'customer_place',default="")
            data['mobile_no'] = fetch_value_or_none(c,'mobile_no',default="")
            data['discount_percentage'] = fetch_value_or_none(c,'discount_percentage',default="")
            data['gst_no'] = fetch_value_or_none(c,'gst_no',default="")


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
            with open('app/templates/invoice.html', 'r') as file:
                html_string = file.read()

            # Render the template with data
            template = Template(html_string)

            html_out = template.render(context=context)



            # pdfkit.from_string(html_string, 'out.pdf',options=options,configuration=configuration,css=css)
            pdf_binary = pdfkit.from_string(html_out, False,options=options,configuration=configuration)

            if 'download_id' in request.args:
                # Create a file-like object from the PDF binary
                pdf_stream = io.BytesIO(pdf_binary)
        
                # Send the file as a download
                return send_file(pdf_stream, as_attachment=True, download_name=f"{data['customer_name']} ({data['invoice_date']}).pdf")

            output_pdf_base64 = b64encode(pdf_binary).decode('utf-8')

            context_2 = {
                "output_pdf_base64":output_pdf_base64,
                "download_id":data['id'],
                "customer_name":data['customer_name'],
                "fetch_company_details":fetch_company_details,
            }

            return render_template('view_invoice.html',context=context_2)
        else:
            return render_template("404.html")

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
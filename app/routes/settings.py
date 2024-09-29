from flask import Blueprint,render_template,redirect,current_app,request,flash
from flask_login import login_required
from app.models.models import Users,Company
from app import db
from base64 import b64encode

settings_blueprint = Blueprint('settings_blueprint', __name__)


@settings_blueprint.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    try:
        fetch_company_details = Company.query.first()

        context = {
            'fetch_company_details':fetch_company_details,
            'ADMIN_EMAIL':current_app.config['ADMIN_EMAIL'],
        }

        if request.method == "POST":
            company_name = request.form.get('company_name',None)
            company_gst_no = request.form.get('company_gst_no',None)


            company_logo_file =  request.files['company_logo_file']
            company_favicon_file =  request.files['company_favicon_file']

            if company_logo_file:
                # Read the file content in binary format
                company_logo_file_data = company_logo_file.read()

                # Convert the file data to a base64-encoded string
                company_logo_base64_encoded_data = b64encode(company_logo_file_data).decode('utf-8')

                fetch_company_details.company_logo = company_logo_base64_encoded_data

            if company_favicon_file:
                # Read the file content in binary format
                company_favicon_file_data = company_favicon_file.read()

                # Convert the file data to a base64-encoded string
                company_favicon_file_base64_encoded_data = b64encode(company_favicon_file_data).decode('utf-8')

                fetch_company_details.company_favicon = company_favicon_file_base64_encoded_data


            fetch_company_details.company_name = company_name
            fetch_company_details.company_gst_no = company_gst_no
            db.session.commit()

            flash('Company details successfully updated','success')
            return redirect('/settings')

        return render_template('settings.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
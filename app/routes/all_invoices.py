from flask import Blueprint,render_template,redirect,current_app,request,flash
from app.models.models import Invoices
import json
from flask_login import login_required

all_invoices_blueprint = Blueprint('all_invoices_blueprint', __name__)


@all_invoices_blueprint.route('/all_invoices')
@login_required
def all_invoices():
    try:
        data = []

        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=25, type=int)

        if per_page > 100:
            per_page = 100

        fetch_all_invoices = Invoices.query.filter(Invoices.is_gst == False).order_by(Invoices.invoice_no.desc()).paginate(page=page, per_page=per_page)

        for fai in fetch_all_invoices.items:
            new_data = {}
            for column in fai.__table__.columns:

                column_value = (getattr(fai, column.name))

                if not column_value:
                    column_value = ''


                new_data[column.name] = column_value
            
            invoice_json = getattr(fai, 'invoice_json',{})

            if invoice_json:
                new_data['invoice_json'] = json.loads(invoice_json)
            else:
                new_data['invoice_json'] = {}
                
            invoice_date = getattr(fai, 'invoice_date',None)
            if invoice_date:
                new_data['invoice_date'] = f"{invoice_date.day}/{invoice_date.month}/{invoice_date.year}"
            else:
                new_data['invoice_date'] = None

            data.append(new_data)
        
        context = {
            "data_items":data,
            "pagination":fetch_all_invoices,
            "page":page,
            "per_page":per_page,
            "total_pages":fetch_all_invoices.pages,
            "total_records":fetch_all_invoices.total,
        }
        
        return render_template('all_invoices.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


@all_invoices_blueprint.route('/all_gst_invoices')
@login_required
def all_gst_invoices():
    try:
        data = []

        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=25, type=int)

        if per_page > 100:
            per_page = 100

        fetch_all_invoices = Invoices.query.filter(Invoices.is_gst == True).order_by(Invoices.invoice_no.desc()).paginate(page=page, per_page=per_page)

        for fai in fetch_all_invoices.items:
            new_data = {}
            for column in fai.__table__.columns:

                column_value = (getattr(fai, column.name))

                if not column_value:
                    column_value = ''


                new_data[column.name] = column_value
            
            invoice_json = getattr(fai, 'invoice_json',{})

            if invoice_json:
                new_data['invoice_json'] = json.loads(invoice_json)
            else:
                new_data['invoice_json'] = {}
                
            invoice_date = getattr(fai, 'invoice_date',None)
            if invoice_date:
                new_data['invoice_date'] = f"{invoice_date.day}/{invoice_date.month}/{invoice_date.year}"
            else:
                new_data['invoice_date'] = None

            data.append(new_data)
        
        context = {
            "data_items":data,
            "pagination":fetch_all_invoices,
            "page":page,
            "per_page":per_page,
            "total_pages":fetch_all_invoices.pages,
            "total_records":fetch_all_invoices.total,
        }
        
        return render_template('all_gst_invoices.html',context=context)

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500
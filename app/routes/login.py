from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for,session
from app import oauth,login_manager,db,app
import os
from dotenv import load_dotenv
load_dotenv()
from authlib.common.security import generate_token
from app.models.models import Users,Company
from flask_login import login_user,current_user
import ast
from datetime import datetime

login_blueprint = Blueprint('login_blueprint', __name__,template_folder='templates')


@app.before_request
def initialize_database():
    with app.app_context():
        db.create_all()

        # Check if there are any records in the Company table
        if Company.query.first() is None:
            try:
                with open('app/static/images/dummy_logo_base64.txt', 'r') as f:
                    dummy_img = f.read()
            except Exception as e:
                dummy_img = None
                app.logger.error(f"Error reading dummy image file: {e}")

            # Add dummy data
            dummy_company = Company(
                company_name='Dummy Company',
                company_gst_no='DUMMY123456',
                company_logo=dummy_img,
                company_favicon=dummy_img,
                date_time_added=datetime.now()
            )
            db.session.add(dummy_company)
            db.session.commit()
            app.logger.info("Dummy company data added.")

            # app.logger.info("Company table already has records.")

@login_blueprint.route('/login')
def login():
    try:

        return render_template('login.html')

    except Exception as e:
        current_app.logger.error(f"{str(e)} WHICH_API = {request.path}", exc_info=True)
        flash(e,'danger')
        return redirect('500.html'), 500


@login_blueprint.route('/google/')
def google():

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('login_blueprint.google_auth', _external=True,_scheme="https")
    # print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@login_blueprint.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    google_account_json = oauth.google.parse_id_token(token, nonce=session['nonce'])
    # session['user'] = user
    # print(" Google User ", google_account_json)
    email = google_account_json.get('email',None)
    name = google_account_json.get('name',None)

    ADMIN_EMAILS = os.getenv('ADMIN_EMAILS',None)

    # Convert the string to a list if it's not None
    if ADMIN_EMAILS:
        ADMIN_EMAIL_LIST = ADMIN_EMAILS.split(',')
    else:
        ADMIN_EMAIL_LIST = []

    check_user = Users.query.filter(Users.email == email).first()
    if email:
        if email not in ADMIN_EMAIL_LIST:
            if not check_user:
                user_try_to_login = Users(name = name,email=email,google_account_json=str(google_account_json))
                db.session.add(user_try_to_login)
                db.session.commit()
            else:
                check_user.name = name
                check_user.google_account_json = str(google_account_json)
                db.session.commit()
            flash('You are not authorize user','error')
            return redirect('/')
        else:
            if not check_user:
                admin_user_try_to_login = Users(name = name,email=email,google_account_json=str(google_account_json),logged_in=True)
                db.session.add(admin_user_try_to_login)
                db.session.commit()
                login_user(admin_user_try_to_login)
            else:
                check_user.name = name
                check_user.google_account_json = str(google_account_json)
                check_user.logged_in = True
                db.session.commit()
                login_user(check_user)
            flash('LOGIN SUCCESSFUL','success')
            return redirect('/')
    else:
        flash('Email not found, Please contact developer!','error')
        return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))


@login_blueprint.app_context_processor
def inject_user():
    # Ensure the attribute exists and is not None before trying to load JSON
    google_account_json_str = getattr(current_user, 'google_account_json', None)
    if google_account_json_str:
        try:
            current_user.google_account_json =ast.literal_eval(google_account_json_str)
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            current_user.google_account_json = {}
    else:
        current_user.google_account_json = {}
    
    return {'current_user': current_user}

@login_blueprint.app_context_processor
def inject_company_details():
    with db.session.no_autoflush:  # Prevent premature autoflush
        fetch_company_details = Company.query.first()
        return {'fetch_company_details': fetch_company_details}

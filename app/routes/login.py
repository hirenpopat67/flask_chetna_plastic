from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for,session
from app import oauth,login_manager,db
import os
from dotenv import load_dotenv
load_dotenv()
from authlib.common.security import generate_token
from app.models.models import Users,Company
from flask_login import login_user,current_user
import ast
from base64 import b64encode

login_blueprint = Blueprint('login_blueprint', __name__,template_folder='templates')


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

    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL',None)

    check_user = Users.query.filter(Users.email == email).first()
    if email:
        if email != ADMIN_EMAIL:
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
                user_try_to_login = Users(name = name,email=email,google_account_json=str(google_account_json),logged_in=True)
                db.session.add(user_try_to_login)
                db.session.commit()
                login_user(check_user)
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

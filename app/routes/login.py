from flask import Blueprint,render_template,redirect,current_app,request,flash,url_for,session
from app import oauth,login_manager,db
import os
from dotenv import load_dotenv
load_dotenv()
from authlib.common.security import generate_token
from app.models.models import Users
from flask_login import login_user,current_user

login_blueprint = Blueprint('login_blueprint', __name__)


@login_blueprint.route('/')
def login():
    try:

        db.create_all()

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
    user_try_to_login = Users(
        google_account_json=str(google_account_json)
    )
    db.session.add(user_try_to_login)
    db.session.commit()
    email = google_account_json.get('email',None)
    if email:
        check_user = Users.query.filter(Users.email == email).first()

        if not check_user:
            flash('You are not authorize user','error')
            return redirect('/')
        else:
            name = google_account_json.get('name',None)
            check_user.name = name
            check_user.google_account_json = str(google_account_json)
            db.session.commit()

            login_user(check_user)
            flash('LOGIN SUCCESSFUL','success')
            return redirect('/all_invoices')
    else:
        flash('Something went wrong','error')
        return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))


@login_blueprint.app_context_processor
def inject_user():
    return {'current_user': current_user}
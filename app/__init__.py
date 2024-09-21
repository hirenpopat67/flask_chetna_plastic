from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()
from importlib import import_module
import logging
from logging.handlers import  RotatingFileHandler
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager

def create_env_file():
    try:
        file_name = ".env"
        file_path = os.path.join(os.getcwd(), file_name)

        if not os.path.exists(file_path):
            print("Creating .env file...")
            print(".env File Is Created...")
            print("Please Update The .env File Variables Now... & Run the App")
            with open(file_path, 'w') as f:
                f.write(
''' # Flask App Settings
SECRET_KEY=
SQLALCHEMY_DATABASE_URI=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
ADMIN_EMAILS=
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
''')
    
    except Exception as e:
        print("Some Error Occurred", e)

app = Flask(__name__,static_folder='static',template_folder='templates')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','Flask_app_secret........')
SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
if not SQLALCHEMY_DATABASE_URI or SQLALCHEMY_DATABASE_URI == '':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chetna_plastic.db'

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_blueprint.login'


def register_blueprints(app):

    folder_list = ['routes']

    for folder in folder_list:
    
        for filename in os.listdir(f'app/{folder}/'):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                blueprint_module = import_module(f'app.{folder}.{module_name}')
                try:
                    blueprint = getattr(blueprint_module, f'{module_name}_blueprint')
                    app.register_blueprint(blueprint)
                except Exception as e:
                    app.logger.exception(f"Failed to register blueprint for file: {module_name} Error: {str(e)}")



try:
    if not os.path.exists('./logs'):
        os.mkdir('./logs')

    file_handler = RotatingFileHandler("./logs/ChetnaPlastic.log",maxBytes=200000, backupCount=5)

    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [path = %(pathname)s:%(lineno)d]'))

    file_handler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    app.logger.info('ChetnaPlastic startup')
except:
    app.logger.exception("Logging is Disabled!")
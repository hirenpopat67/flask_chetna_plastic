from app import app,create_env_file,register_blueprints
from app.routes.errorhandler import page_not_found

register_blueprints(app)
app.register_error_handler(404, page_not_found)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=2002, keyfile='key.pem', certfile='cert.pem')
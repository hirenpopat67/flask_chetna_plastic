from app import app,create_env_file,register_blueprints,db
from app.routes.errorhandler import page_not_found

register_blueprints(app)
app.register_error_handler(404, page_not_found)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0',port=2002, ssl_context=('cert.pem', 'key.pem'))
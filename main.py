from app import app,create_env_file,register_blueprints

if __name__ == '__main__':
    register_blueprints(app)
    create_env_file()
    app.run(debug=True,host='0.0.0.0')
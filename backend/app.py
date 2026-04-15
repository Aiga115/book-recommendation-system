from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    JWTManager(app)

    # Register blueprints
    from routes.auth  import auth_bp
    from routes.admin import admin_bp
    from routes.user  import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables if they don't exist
    app.run(debug=True)
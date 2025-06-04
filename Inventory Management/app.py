from flask import Flask
from flask_login import LoginManager
from models import db
from admin import admin_bp
from user import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Inventory_Management.db'
app.config['SECRET_KEY'] = ''

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Register routes
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

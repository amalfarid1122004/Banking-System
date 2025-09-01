from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes.auth_routes import auth_bp
from routes.account_routes import account_bp
from routes.transaction_routes import transaction_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['JWT_SECRET_KEY'] = 'secret123'

db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

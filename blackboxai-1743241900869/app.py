from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///osteopath.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes after db initialization to avoid circular imports
from routes.patients import patients_bp
from routes.consultations import consultations_bp
from routes.invoices import invoices_bp

app.register_blueprint(patients_bp, url_prefix='/patients')
app.register_blueprint(consultations_bp, url_prefix='/consultations')
app.register_blueprint(invoices_bp, url_prefix='/invoices')

if __name__ == '__main__':
    app.run(debug=True)
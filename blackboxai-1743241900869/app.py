from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='./frontend/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///osteopath.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Patient, Consultation, Invoice

@app.route('/')
def index():
    patients = Patient.query.count()
    consultations = Consultation.query.count()
    total_invoices = Invoice.query.count()
    paid_invoices = Invoice.query.filter_by(status='paid').count()
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    upcoming_consultations = Consultation.query.filter(Consultation.date >= datetime.now()).order_by(Consultation.date).limit(5).all()
    
    return render_template('index.html', 
                         patients_count=patients,
                         consultations_count=consultations,
                         total_invoices=total_invoices,
                         paid_invoices=paid_invoices,
                         recent_patients=recent_patients,
                         upcoming_consultations=upcoming_consultations)

# Import routes after db initialization to avoid circular imports
from routes.patients import patients_bp
from routes.consultations import consultations_bp
from routes.invoices import invoices_bp

app.register_blueprint(patients_bp, url_prefix='/patients')
app.register_blueprint(consultations_bp, url_prefix='/consultations')
app.register_blueprint(invoices_bp, url_prefix='/invoices')

if __name__ == '__main__':
    app.run(debug=True)
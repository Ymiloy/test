from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class JobOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=True)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<JobOffer {self.title}>'

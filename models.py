from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Service(db.Model):
    """Модель для AI-услуг"""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Цена в рублях
    currency = db.Column(db.String(3), default='RUB')
    category = db.Column(db.String(50), nullable=False)
    completion_time = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Преобразует объект в словарь для JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'currency': self.currency,
            'category': self.category,
            'completion_time': self.completion_time,
            'created_at': self.created_at.isoformat()
        }


class CompanyInfo(db.Model):
    """Модель для информации о компании"""
    __tablename__ = 'company_info'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    founded_year = db.Column(db.Integer, nullable=False)
    team_size = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Преобразует объект в словарь для JSON"""
        return {
            'company_name': self.company_name,
            'description': self.description,
            'founded_year': self.founded_year,
            'team_size': self.team_size,
            'contact': {
                'email': self.email,
                'phone': self.phone
            },
            'updated_at': self.updated_at.isoformat()
        }

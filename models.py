from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import check_password_hash
from sqlalchemy.sql import func

# Initialize metadata
metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)

    # Exclude relationships to avoid recursion
    serialize_rules = ('-password', '-records.user', '-payments.user', '-school_fees.user')

    records = db.relationship('Record', back_populates='user', lazy='dynamic')
    payments = db.relationship('Payment', back_populates='user', lazy='dynamic')
    school_fees = db.relationship('SchoolFees', back_populates='user', lazy='dynamic')

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    def as_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email
        }
        if include_relations:
            data['records'] = [record.as_dict() for record in self.records.all()]
            data['payments'] = [payment.as_dict() for payment in self.payments.all()]
            data['school_fees'] = [school_fee.as_dict() for school_fee in self.school_fees.all()]
        return data


class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')

    serialize_rules = ('-records.book', '-inventory.book')

    records = db.relationship('Record', back_populates='book', lazy='dynamic')
    inventory = db.relationship('Inventory', back_populates='book', lazy='dynamic')

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'status': self.status
        }


class Record(db.Model, SerializerMixin):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-book.records', '-user.records', '-penalties.record')

    penalties = db.relationship('Penalty', back_populates='record', lazy='dynamic')
    book = db.relationship('Book', back_populates='records')
    user = db.relationship('User', back_populates='records')

    def as_dict(self):
        return {
            'id': self.id,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d') if self.borrow_date else None,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'book_id': self.book_id,
            'user_id': self.user_id
        }


class Penalty(db.Model, SerializerMixin):
    __tablename__ = 'penalties'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)

    record = db.relationship('Record', back_populates='penalties')

    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'status': self.status,
            'record_id': self.record_id
        }

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    transaction_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    payment_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

    user = db.relationship('User', back_populates='payments')

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'payment_date': self.payment_date.strftime('%Y-%m-%d') if self.payment_date else None
        }

class SchoolFees(db.Model, SerializerMixin):
    __tablename__ = 'school_fees'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    user = db.relationship('User', back_populates='school_fees')

    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'status': self.status,
            'user_id': self.user_id
        }

class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), unique=True)
    current_stock = db.Column(db.Integer, nullable=False)

    book = db.relationship('Book', back_populates='inventory')

    def as_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'current_stock': self.current_stock
        }

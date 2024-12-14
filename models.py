from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
# from datetime import datetime
from sqlalchemy.sql import func
from flask_bcrypt import check_password_hash

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

    serialize_rules = ('-password',)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    # books = db.relationship('Book', backref='user', lazy=True)
    records = db.relationship('Record', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    # penalties = db.relationship('Penalty', backref='user', lazy=True)
    school_fees = db.relationship('SchoolFees', backref='user', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            # 'books': [book.as_dict() for book in self.books],
            'records': [record.as_dict() for record in self.records],
            'payments': [payment.as_dict() for payment in self.payments],
            # 'penalties': [penalty.as_dict() for penalty in self.penalties],
            'school_fees': [school_fee.as_dict() for school_fee in self.school_fees]
        }
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    records = db.relationship('Record', backref='book', lazy=True)
    inventory = db.relationship('Inventory', backref='book', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'status': self.status,
            # 'user_id': self.user_id,
            'records': [record.as_dict() for record in self.records],
            'inventory': [inventory.as_dict() for inventory in self.inventory]
        }

class Record(db.Model, SerializerMixin):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    penalties = db.relationship('Penalty', backref='record', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d') if self.borrow_date else None,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'penalties': [penalty.as_dict() for penalty in self.penalties]
        }

class Penalty(db.Model, SerializerMixin):
    __tablename__ = 'penalties'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    # book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            # 'book_id': self.book_id,
            # 'user_id': self.user_id,
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

    def as_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'current_stock': self.current_stock
        }

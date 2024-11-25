from models import db, Book
from app import app

with app.app_context():

    print('Start seeding...')

    print('Deleting data...')
    Book.query.delete()

    print("Creating books...")

    books = [
        Book(title= 'A Doll\'s house', author= 'Henrik Ibsen', category= 'Set Book', status= 'available')
    ]

    db.session.add_all(books)
    db.session.commit()
    print('books seeded')
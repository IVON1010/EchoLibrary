from models import db, Book
from flask_restful import Resource, reqparse



class BookResource(Resource):
    # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True, help='title is required')
    parser.add_argument('author', required=True, help='author is required')
    parser.add_argument('category', required=True, help='category is required')
    parser.add_argument('status', required=True, help='status is required')
    # parser.add_argument('user_id', required=True, help='user_id is required', type=int)

    def get(self, id=None):
        if id:
            book = Book.query.filter_by(id=id).first()

            if book == None:
                return {"message": "Book not found"}, 404

            return book.as_dict()
        
        else:
            books = Book.query.all()
            return [book.as_dict() for book in books]
        


    def post(self):
        data = BookResource.parser.parse_args()
        
        book = Book(**data)

        db.session.add(book)

        db.session.commit()

        return {"message": "Book created successfully"}, 201
    
    
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()

        if book is None:
            return {"message": "Book not found"}, 404
        
        db.session.delete(book)
        db.session.commit()

        return {"message": "Book deleted successfully"}, 200
    
    def put(self, id):
        book = Book.query.filter_by(id=id).first()

        if book is None:
            return {"message": "Book not found"}, 404
        
        data = BookResource.parser.parse_args()

        book.status = data['status']

        db.session.commit()

        return {"message": "Book updated successfully"}
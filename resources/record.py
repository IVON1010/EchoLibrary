from flask_restful import Resource, reqparse, inputs
from models import db, Record


class RecordResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('borrow_date', required=True, type=inputs.date, help='borrow_date required (YYYY-MM-DD)')
    parser.add_argument('due_date', required=True, type=inputs.date, help='due_date required (YYYY-MM-DD)')
    parser.add_argument('return_date', required=True, type=inputs.date, help='return_date required (YYYY-MM-DD)')
    parser.add_argument('book_id', required=True, type=int, help='book_id required')
    parser.add_argument('user_id', required=True, type=int, help='user_id required')

    def get(self, id=None):
        if id:
            record = Record.query.filter_by(id=id).first()

            if record is None:
                return {"message": "Record not found"}, 404
            
            return record.as_dict()
        

        else:
            records = Record.query.all()
            return [record.as_dict() for record in records], 200

    
    def post(self):
        data = RecordResource.parser.parse_args()


        # Create a new record entry
        record = Record(**data)
        db.session.add(record)
        db.session.commit()

        return {"message": "Record created successfully"}, 201
    

    def delete(self, id):
        record = Record.query.filter_by(id=id).first()

        if record is None:
            return {"message": "Record not found"}, 404
        
        db.session.delete(record)
        db.session.commit()

        return {"message": "Record deleted successfully"}, 204
    

    def put(self, id):
        record = Record.query.filter_by(id=id).first()

        if record is None:
            return {"Record not found"}
        
        data = RecordResource.parser.parse_args()

        record.due_date = data['due_date']

        db.session.commit()
        
        return {"message": "Record successfully updated"}

    
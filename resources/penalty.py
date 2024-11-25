from models import db, Penalty
from flask_restful import Resource, reqparse


class PenaltyResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', required=True, type=int, help='amount is required')
    parser.add_argument('status', required=True, help='status is required')
    parser.add_argument('record_id', required=True, type=int, help='record_id is required')


    def get(self, id=None):
        if id:
            penalty = Penalty.query.filter_by(id=id).first()

            if id == None:
                return {"message": "Penalty not found"}
            
            return penalty.as_dict()
        
        else:
            penalties = Penalty.query.all()
            return [penalty.as_dict() for penalty in penalties]
        

    def post(self):
        data = PenaltyResource.parser.parse_args()

        penalty = Penalty(**data)
        db.session.add(penalty)
        db.session.commit()

        return {"message": "Penalty added successfully"}, 201
    
    def delete(self, id):
        penalty = Penalty.query.filter_by(id=id).first()

        if penalty is None:
            return {"message": "Penalty not found"}, 404

        db.session.delete(penalty)
        db.session.commit()

        return {"message": "Penalty deleted successfully"}, 204
    
    def put(self, id):
        penalty = Penalty.query.filter_by(id=id).first()

        if penalty is None:
            return {"message": "Penalty not found"}, 404
        
        data = PenaltyResource.parser.parse_args()

        penalty.amount = data['amount']
        penalty.status = data['status']

        db.session.commit()

        return {"message": "Penalty updated successfully"}, 200
        
    
from models import db, Payment
from flask_restful import Resource, reqparse, inputs


class PaymentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, type=int, help='user_id is required')
    parser.add_argument('transaction_id', required=True, type=id, help='transaction_id is required')
    parser.add_argument('amount', required=True, type=int, help='amount is required')
    parser.add_argument('status', required=True, help='status is required')
    parser.add_argument('payment_date', required=True, type=inputs.date, help='user_id is required (YYYY-MM-DD)')


    def get(self, id):
        if id:
            payment = Payment.query.filter_by(id=id).first()
            
            if id == None:
                return {"message": "Payment not found"}
            
            return payment.as_dict()
        
        else:
            payments = Payment.query.all()
            return [payment.as_dict() for payment in payments]
        

    def post(self):
        data = PaymentResource.parser.parse_args()

        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()

        return {"message": "Payment created successfully"}, 201
    
    def delete(self, id):
        payment = Payment.query.filter_by(id=id).first()

        if payment is None:
            return {"message": "Payment deleted successfully"}, 404
        
        db.session.delete(payment)
        db.session.commit()

        return {"message": "Payment deleted successfully"}, 204
    
    def put(self, id):
        payment = Payment.query.filter_by(id=id).first()

        if payment is None:
            return {"message": "Payment deleted successfully"}, 404
        
        data = PaymentResource.parser.parse_args()

        payment.status = data['status']
        payment.amount = data['amount']
        payment.transaction_id = data['transaction_id']

        db.session.commit()

        return {"message": "Payment updated successfully"}



from models import db, Payment
from flask_restful import Resource, reqparse, inputs
from paystackapi.transaction import Transaction
from paystackapi.paystack import Paystack
import os


PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_fd04b278f954772e66ae6e0b1e93914d7f0de3bd")
paystack = Paystack(secret_key=PAYSTACK_SECRET_KEY)


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



class PaymentResource(Resource):
    # Parser for payment details
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', required=True, type=int, help='user_id is required')
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('amount', required=True, type=int, help='amount is required')

    def post_payment(self):
        data = self.parser.parse_args()

        try:
            # Convert amount to kobo (for NGN) or smallest currency unit
            amount = data['amount'] * 100

            # Initialize the transaction
            response = Transaction.initialize(
                reference=f"txn_{data['user_id']}_{data['amount']}",
                amount=amount,
                email=data['email']
            )

            # Return the authorization URL to the frontend
            if response['status']:
                return {
                    "message": "Payment initiated successfully",
                    "authorization_url": response['data']['authorization_url'],
                    "reference": response['data']['reference']
                }, 200
            else:
                return {"message": "Payment initialization failed", "error": response['message']}, 400

        except Exception as e:
            return {"message": "An error occurred during payment initialization", "error": str(e)}, 500
        


    def verify_payment(self, reference):
        try:
            # Verify the transaction
            response = Transaction.verify(reference=reference)

            if response['status'] and response['data']['status'] == 'success':
                return {"message": "Payment successful", "data": response['data']}, 200
            else:
                return {"message": "Payment verification failed", "error": response['message']}, 400

        except Exception as e:
            return {"message": "An error occurred during payment verification", "error": str(e)}, 500

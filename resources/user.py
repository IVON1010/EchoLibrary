from models import db, User
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

class UserResource(Resource):
    # Define the parser for both user data and pagination
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='name is required')
    parser.add_argument('username', required=True, help='username is required')
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')

    # Pagination parser
    pagination_parser = reqparse.RequestParser()
    pagination_parser.add_argument('page', type=int, help='Page number', default=1)
    pagination_parser.add_argument('per_page', type=int, help='Users per page', default=20)

    @jwt_required()
    def get(self, id=None):
        current_user_id = get_jwt_identity()

        # If an id is provided, return that user
        if id:
            user = User.query.filter_by(id=id).first()
            if user:
                return {"message": "User found", "user": user.to_dict()}, 200
            return {"message": "User not found"}, 404
        
        # If no id is provided, return the current user's profile
        else:
            user = User.query.get(current_user_id)
            if user:
                return {"message": "User profile fetched successfully", "user": user.to_dict()}, 200
            return {"message": "User not found"}, 404

    
    @jwt_required()
    def get_all_users(self):
        # Parse the pagination arguments
        args = UserResource.pagination_parser.parse_args()
        page = args['page']
        per_page = args['per_page']

        # Get the users with pagination
        users = User.query.paginate(page, per_page, False)

        # Return the users along with pagination metadata
        return {
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }, 200

    def post(self):
        data = UserResource.parser.parse_args()
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already exists", "status": "fail"}, 422
        data['password'] = generate_password_hash(data['password']).decode('utf-8')
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully", "user": user.to_dict()}, 201

    @jwt_required()
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 204

    @jwt_required()
    def put(self, id):
        data = UserResource.parser.parse_args()
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"message": "User not found"}, 404
        user.name = data['name']
        user.username = data['username']
        user.email = data['email']
        user.password = generate_password_hash(data['password']).decode('utf-8')
        db.session.commit()
        return {"message": "User successfully updated", "user": user.to_dict()}, 200

class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')

    def post(self):
        data = LoginResource.parser.parse_args()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            return {
                "message": "Login successful",
                "access_token": access_token,
                "user": user.to_dict()
            }, 200
        return {"message": "Invalid email/password", "status": "fail"}, 403

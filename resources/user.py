from models import db, User
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='name is required')
    parser.add_argument('username', required=True, help='username is required')
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')

    @jwt_required()
    def get(self, id=None):
        if id:
            user = User.query.filter_by(id=id).first()

            if user is None:
                return { "message": "user doesn't exist"}, 404
            
            return user.as_dict()
        
        else:
            users = User.query.all()
            return [user.as_dict() for user in users], 200
        
    @jwt_required()
    def post(self):
        data = UserResource.parser.parse_args()

        #print(generate_password_hash(data['password']))

        data['password'] = generate_password_hash(data['password']).decode('utf-8')

        #print(data)

        # ensure email eixst
        email = User.query.filter_by(email=data['email']).first()

        if email:
            return { "message" : "email already exists", "status": "fail"}, 422

        user=User(**data)
        db.session.add(user)
        db.session.commit()

        return { "message": "user created successfully", "status": "success", "user": user.to_dict()}, 201
    
    @jwt_required()
    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return {"message": "User not found"}, 404
        
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 204
    
    @jwt_required()
    def put(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return {"message": "User not found"}, 404
        
        data = UserResource.parser.parse_args()

        user.name = data['name']
        user.username = data['username']
        user.email = data['email']
        user.password = generate_password_hash(data['password']).decode('utf-8')

        db.session.commit()

        return {"message": "User successfully updated"}
    

class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')

    def post(self):
        data = LoginResource.parser.parse_args()

        #print(data)

        # 1. Try to retrieve user with provided email
        user = User.query.filter_by(email = data['email']).first()

        # 2. check if user exists
        if user:
            # 3. password verification
            if check_password_hash(user.password, data['password']):
                access_token =create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
                return {
                    "message": "Login Successful",
                    "status": "success",
                    "access_token": access_token,
                    "user": user.to_dict()
                }, 200
                #return {"message": "Login Successful", "status": "Success", "user": user.to_dict()}, 200
            else:
                {"message": "Invalid email/password", "status": "fail"}, 403
            
        else:
            return {"message": "Invalid password/email", 'status': "fail"}, 403
        
    @jwt_required()
    def get(self, id=None):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if user:
            {"message": "User profile fetched successfully", "status": "success", "user": user.to_dict()}, 200
        else:
            {"message": "User not found", "status": "fail"}, 404
        

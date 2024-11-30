from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, marshal, abort, fields, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres.efnrejuwcbrarhvjddcv:Tanoj%40190605@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

api=Api(app)
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, help='Name of the user',required=True)
user_args.add_argument('email', type=str, help='Email of the user',required=True)


user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class user_edit(Resource):
    @marshal_with(user_fields)
    def get(self,user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404,message='User not found')
        return user, 200

    @marshal_with(user_fields)
    def put(self,user_id):
        args = user_args.parse_args()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404,message='User not found')
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user, 200

    def delete(self,user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404,message='User not found')
        db.session.delete(user)
        db.session.commit()
        return 'Successfully deleted user', 204

class user(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = User(name=args['name'],email=args['email'])
        if User.query.filter_by(email=args['email']).first():
            abort(409,message='User already exists')

        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users, 200


api.add_resource(user,'/user')
api.add_resource(user_edit,'/user/<int:user_id>')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User(name={self.name},email={self.email})"

@app.route('/')
def sample():
    return 'Hello Rahul!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
        print('Database created!')

    app.run(debug=True)

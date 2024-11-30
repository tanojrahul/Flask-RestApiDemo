from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, marshal, abort, fields, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite3'
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

class user(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = User(name=args['name'],email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users, 200


api.add_resource(user,'/user')

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

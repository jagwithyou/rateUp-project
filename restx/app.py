from flask import Flask, request
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy 


# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = '%(DB_TYPE)s://%(DB_USER)s:%(DB_PWD)s@%(DB_HOST)s/%(DB_SCHEMA)s' \
    % {
        'DB_TYPE': 'postgresql',
        'DB_USER': 'infjteyssjsgvy',
        'DB_PWD': '87d15501cde43eb71b6b1d3d677e2e6e6ef7da887aafc48092b794b6b8ecaa21',
        'DB_HOST': 'ec2-54-82-205-3.compute-1.amazonaws.com',
        'DB_SCHEMA': 'd2chf1k079jot0'
    }

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)

api = Api(app, version='1.0', title='RATEITUP API',
    description='A simple Rating system',
)

ns = api.namespace('users', description='User management operations')
ns_games = api.namespace('games', description='Game operations')
ns_ratings = api.namespace('ratings', description='Game Rating operations')

user = api.model('User', {
    # 'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='The task details'),
    'email': fields.String(required=True, description='The task details'),
    'password': fields.String(required=True, description='The task details')
    
})

profile = api.model('profile', {
    # 'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='The task details')
    
})

game = api.model('User', {
    # 'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='The task details'),
    'description': fields.String(required=True, description='The task details'),
    'filename': fields.String(required=True, description='The task details')
    
})

rating = api.model('GameRating', {
    # 'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'rating': fields.String(required=True, description='The task details'),
    'message': fields.String(required=True, description='The task details'),
    'ratedby': fields.String(required=True, description='The task details'),
    'gameid': fields.String(required=True, description='The task details')
    
})

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Games(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    filename = db.Column(db.String)

class GameRating(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    rating = db.Column(db.String)
    message = db.Column(db.String)
    ratedby = db.Column(db.String)
    gameid = db.Column(db.Integer)

@ns.route('/')
class UserManagement(Resource):
    @ns.expect(user)
    @ns.marshal_list_with(user)
    def post(self):
        '''Create a user'''
        print(request.json)
        user = Users()
        # user.id = request.json.id
        user.name = request.json["name"]
        user.email = request.json["email"]
        user.password = request.json["password"]
        db.session.add(user)
        return user
    
    @ns.marshal_list_with(user)
    def get(self):
        '''List all users'''
        users = Users.query.all()
        return users

@ns.route('/<int:id>')
@ns.param('id', 'The task identifier')
class UserManagementSingle(Resource):
    @ns.expect(user)
    @ns.marshal_list_with(user)
    def put(self, id):
        '''Update user'''
        print(request.json)
        user = Users.query.get(id)
        # user.id = request.json.id
        user.name = request.json["name"]
        user.email = request.json["email"]
        user.password = request.json["password"]
        db.session.add(user)
        return user
    
    @ns.marshal_list_with(user)
    def get(self, id):
        '''Get Specific user'''
        users = Users.query.get(id)
        return users
    
    def delete(self, id):
        '''delete specific user'''
        users = Users.query.get(id)
        db.session.delete(users)
        return {"message": "Record Deleted"}


@ns.route('/<int:id>/profile')
@ns.param('id', 'The task identifier')
class UserManagementSingle(Resource):
    @ns.marshal_list_with(profile)
    def get(self, id):
        '''Get profile'''
        users = Users.query.get(id)
        return users
    
    def delete(self, id):
        '''delete specific user'''
        users = Users.query.get(id)
        db.session.delete(users)
        return {"message": "Record Deleted"}


@ns_games.route('/')
class GameManagement(Resource):
    @ns_games.expect(game)
    @ns_games.marshal_list_with(game)
    def post(self):
        '''Create a game'''
        print(request.json)
        game = Games()
        # user.id = request.json.id
        game.name = request.json["name"]
        game.description = request.json["description"]
        game.filename = request.json["filename"]
        db.session.add(game)
        return game
    
    @ns_games.marshal_list_with(game)
    def get(self):
        '''List all games'''
        games = Games.query.all()
        return games

@ns_games.route('/<int:id>')
@ns_games.param('id', 'The task identifier')
class GameManagementSingle(Resource):
    @ns_games.expect(rating)
    @ns_games.marshal_list_with(rating)
    def put(self, id):
        '''Update game'''
        print(request.json)
        rating = Games.query.get(id)
        print(rating)
        rating.name = request.json["name"]
        rating.description = request.json["description"]
        rating.filename = request.json["filename"]
        db.session.add(rating)
        return rating
    
    @ns_games.marshal_list_with(rating)
    def get(self, id):
        '''Get Specific game'''
        rating = Games.query.get(id)
        return rating

    def delete(self, id):
        '''delete specific game'''
        game = Games.query.get(id)
        db.session.delete(game)
        return {"message": "Record Deleted"}



@ns_ratings.route('/rating')
class GameRatings(Resource):
    @ns_ratings.expect(rating)
    @ns_ratings.marshal_list_with(rating)
    def post(self):
        '''Create a rating'''
        print(request.json)
        rating = GameRating()
        # user.id = request.json.id
        rating.rating = request.json["rating"]
        rating.message = request.json["message"]
        rating.ratedby = request.json["ratedby"]
        rating.gameid = request.json["gameid"]
        db.session.add(rating)
        return rating
    
    @ns_ratings.marshal_list_with(rating)
    def get(self):
        '''List all ratings'''
        ratings = GameRating.query.all()
        return ratings

@ns_ratings.route('rating/<int:id>')
@ns_ratings.param('id', 'The task identifier')
class GameRatingSingle(Resource):
    @ns_ratings.expect(rating)
    @ns_ratings.marshal_list_with(rating)
    def put(self, id):
        '''Update rating'''
        print(request.json)
        rating = GameRating.query.get(id)
        print(rating)
        rating.rating = request.json["rating"]
        rating.message = request.json["message"]
        rating.ratedby = request.json["ratedby"]
        rating.gameid = request.json["gameid"]
        db.session.add(rating)
        db.session.commit()
        return rating
    
    @ns_ratings.marshal_list_with(rating)
    def get(self, id):
        '''Get Specific rating'''
        rating = GameRating.query.get(id)
        return rating
    
    def delete(self, id):
        '''delete specific rating'''
        game_rating = GameRating.query.get(id)
        db.session.delete(game_rating)
        return {"message": "Record Deleted"}


if __name__ == '__main__':
    app.run(debug=True)
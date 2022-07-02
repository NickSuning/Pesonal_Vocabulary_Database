from . import db  #from app package root folder import db
from flask_login import UserMixin #importing user module helping login

class User(db.Model, UserMixin): #define User table in db as db model
    id = db.Column(db.Integer, primary_key = True)  #define primary key column
    user_name = db.Column(db.String(20),unique = True)
    password = db.Column(db.String(10))
    vocabularies = db.relationship('Vocabulary') #referening back to Vocabulary model user_id Column

class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(100))
    meaning = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_time = db.Column(db.DateTime)
    result_score = db.Column(db.Integer)
    result_number = db.Column( db.Integer )
    result_last_voca = db.Column( db.Integer )
    result_test_type = db.Column( db.String(10))
    user_id = db.Column( db.Integer, db.ForeignKey( User.id ) )


from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import camel_to_snake_case
import requests
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)
bcrypt = Bcrypt()
class Type(db.Model):
    __tablename__ = 'types'
    name = db.Column(db.String(),
                     primary_key=True)
    image = db.Column(db.String(),
                      nullable=False)
    pokemon = db.relationship("Pokemon", backref="types")
class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name =  db.Column(db.String(),
                    
                    nullable = False,
                    unique = True)
    # will only select 1 of the multiple types. 
    poke_type = db.Column(db.String(),
                          db.ForeignKey('types.name'))
   
    # selects only 1 image
    image = db.Column(db.String())

    hp = db.Column(db.Integer)
    
    defense = db.Column(db.Integer)
    
    moves = db.relationship("Moves", secondary="pokemon_moves", backref="pokemon")
    
    def __repr__(self):
        return f'<id:{self.id}name:{self.name} >'

   
    

class Moves(db.Model):
    __tablename__ = 'moves'
    id = db.Column(db.Integer(),
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text(),nullable=False)
    move_type = db.Column(db.String(),
                     db.ForeignKey('types.name'))
    power = db.Column(db.Integer,
                      nullable=False)
    priority = db.Column(db.Integer,
                         nullable=False)
    details = db.Column(db.Text())
    type = db.relationship('Type',backref='type')
   

    
    


class PokemonMoves(db.Model):
    _tablename_ = 'pokemoves'
    poke_id = db.Column(db.Integer,db.ForeignKey('pokemon.id'),
                        primary_key=True)
      

    move_id = db.Column(db.Integer,db.ForeignKey('moves.id'),
                        primary_key=True)
    
class Deck(db.Model):
    __tablename__='deck'

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    poke_id = db.Column(db.Integer,db.ForeignKey('pokemon.id'),primary_key=True)
    

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(),nullable=False)
    starter = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False,unique=True)
    deck = db.relationship('Pokemon',secondary='deck',backref='pokemon')
    luckynum = db.Column(db.Integer,nullable=False)
    @classmethod
    def register(cls,username,password,email,starter,luckynum):
        hashed = bcrypt.generate_password_hash(password);
        decoded = hashed.decode('utf8')
        
        
        user = User(username=username, email=email,password=decoded,starter=starter,luckynum=luckynum)
        
        db.session.add(user)
        return user;
        
        

from flask import Flask, json , render_template, jsonify
import requests
from requests.api import request
from werkzeug.utils import redirect

from models import connect_db,Pokemon,db,Moves,PokemonMoves,User,Deck
from forms import Register



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pokemoncardgame'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'YOURSECRETISSAFEWITHME'

connect_db(app)

@app.route('/')
def homepage():
    return redirect('/users')

@app.route('/signup', methods=['GET','POST'])
def register():
    form = Register()
    starters = [(pokemon.id,pokemon.name)for pokemon in Pokemon.query.all() if pokemon.id == 1 or pokemon.id == 4 or pokemon.id == 7]
    form.starter.choices = starters;
    if form.validate_on_submit():
        user = User.register(username=form.username.data,
                             password=form.password.data,email=form.email.data,luckynum=form.luckynum.data,starter=form.starter.data)
        if user: 
            db.session.commit()
            addStarterDeck = Deck(user_id=user.id,poke_id=user.starter)
            db.session.add(addStarterDeck)
            addSpecial = Deck(user_id=user.id,poke_id=user.luckynum)
            db.session.add(addSpecial)
            db.session.commit()
            return redirect('/users')
    else:
        return render_template('form.html',form=form)
@app.route('/users')
def getUsers():
    users=User.query.all();
    
    
    return render_template('users.html',response=users)
@app.route('/users/<int:id>')
def getUser(id):
    user = User.query.get(id);
    return render_template('user.html',response=user)


@app.route('/pokemon')
def home():
    allPokemon = Pokemon.query.all()
    
    
        
    return render_template('pokemon.html',response=allPokemon)

    
@app.route('/pokemon/<int:id>')
def getPokeData(id):
    pokemon = Pokemon.query.get(id)
    moves = pokemon.moves;
    
    type_banner = pokemon.types.image
    return render_template('details.html',response=pokemon, moves=moves, type=type_banner)




@app.route('/moves')
def getAllMoves():
    moves = Moves.query.all();
    
    return render_template('moves.html',response=moves);

@app.route('/moves/<int:id>')
def getMove(id):
    move = Moves.query.get(id);
    return render_template('index.html', response=move);
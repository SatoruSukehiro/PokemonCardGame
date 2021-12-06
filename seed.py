import re
import requests,random
from sqlalchemy.orm import clear_mappers
from werkzeug.wrappers import response
from app import app
from models import Moves, Pokemon,db,PokemonMoves,Type



db.drop_all()
db.create_all()


types = {'grass': "https://pokeguide.neocities.org/Pic/grassicon.png", 'fire': 'https://pokeguide.neocities.org/Pic/fireicon.png','water' : 'https://pokeguide.neocities.org/Pic/watericon.png', 'normal': 'https://pokeguide.neocities.org/Pic/normalicon.png','poison': 'https://pokeguide.neocities.org/Pic/poisonicon.png','fighting': 'https://pokeguide.neocities.org/Pic/fightingicon.png','steel':'https://pokeguide.neocities.org/Pic/steelicon.png', 'ice':'https://pokeguide.neocities.org/Pic/iceicon.png','fairy': 'https://pokeguide.neocities.org/Pic/fairyicon.png' , 'psychic' : 'https://pokeguide.neocities.org/Pic/physicicon.png','dragon':'https://pokeguide.neocities.org/Pic/dragonicon.png','dark':'https://pokeguide.neocities.org/Pic/darkicon.png','ghost':'https://pokeguide.neocities.org/Pic/ghosticon.png','rock': 'https://pokeguide.neocities.org/Pic/rockicon.png','bug':'https://pokeguide.neocities.org/Pic/bugicon.png','flying':'https://pokeguide.neocities.org/Pic/flyingicon.png','ground':'https://pokeguide.neocities.org/Pic/groundicon.png','electric':'https://pokeguide.neocities.org/Pic/electricicon.png'}
for move,image in types.items():
    t = Type(name=move,image=image)
    db.session.add(t)
    db.session.commit();
response = requests.get('https://pokeapi.co/api/v2/pokemon/',params={"limit": 200}).json()
pokemonList = [requests.get(f"{data['url']}").json() for data in response['results']]
for pokemon in  pokemonList: 
     name =  pokemon['name']
     artwork = pokemon['sprites']['other']['official-artwork']['front_default']
     hp = pokemon['stats'][0]['base_stat']
     defense = pokemon['stats'][2]['base_stat']
     type = pokemon['types'][0]['type']['name']
     pokemon = Pokemon(hp=hp,defense=defense, name=name,poke_type=type,   image=artwork)
     db.session.add(pokemon)
     db.session.commit()


movesresponse = requests.get('https://pokeapi.co/api/v2/move',params={"limit": 200}).json()

movesList = [requests.get(f"{data['url']}").json() for data in movesresponse['results']]
for move in movesList:
    name = move['name']
    move_type= move['type']['name']
    power = move['power']  if move['power'] else 10
    priority = move['priority']
    details = move['flavor_text_entries'][0]['flavor_text']
    canLearn = [pokemon['name'] for pokemon in move['learned_by_pokemon']]
    print(details)
    move = Moves(name=name,move_type=move_type,power=power,priority=priority,details=details)
    db.session.add(move)
    db.session.commit()   
    
    for pokemon in canLearn:
        pokemon = Pokemon.query.filter_by(name=pokemon).first()
        if pokemon:
            pokemonMoves= PokemonMoves(poke_id=pokemon.id,move_id=move.id)
            db.session.add(pokemonMoves)
            db.session.commit();



# -*- coding: utf-8 -*-

import argparse
import getpass
import json
import time
from pgoapi import pgoapi

pokemon_list = ["Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash",u"Nidoran♀","Nidorina","Nidoqueen",u"Nidoran♂","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetch'd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr. Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew"]

def init_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')", required=True)
    parser.add_argument("-u", "--username", help="Username", required=True)
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-lat", "--latitude", help="Latitude", required=True)
    parser.add_argument("-long", "--longitude", help="Longitude", required=True)
    parser.add_argument("--reset", action='store_true', default=False)
    config = parser.parse_args()

    if config.auth_service not in ['ptc', 'google']:
        print "Invalid authentication service. Please input 'ptc' or 'google'."
        return None

    if config.__dict__["password"] is None:
        config.__dict__["password"] = getpass.getpass()

    return config

def main():
    config = init_config()
    if not config:
        return

    api = pgoapi.PGoApi()
    api.set_position(float(config.latitude), float(config.longitude), 0.0)

    if not api.login(config.auth_service, config.username, config.password):
        print 'Login failed.'
        return
    print 'Login successful.'

    api.get_inventory()
    response_dict = api.call()
    inventory_list = response_dict['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
    pokemon_count = 0
    for item in inventory_list:
        if 'pokemon_data' in item['inventory_item_data']:
            pokemon = item['inventory_item_data']['pokemon_data']
            if all(k in pokemon for k in ('individual_attack', 'individual_defense' , 'individual_stamina', 'id')):
            	poke_id = pokemon['id']
                species_name = pokemon_list[int(pokemon['pokemon_id']) - 1]
                nickname = pokemon.get('nickname', species_name)
                if config.reset:
                	new_name = species_name
                else:
	                attack = pokemon.get('individual_attack', 0)
	                defense = pokemon.get('individual_defense', 0)
	                stamina = pokemon.get('individual_stamina', 0)
	                percent_perfection = int((float(attack + defense + stamina) / 45.0) * 100.0) 
	                new_name = str(attack) + '/' + str(defense) + '/' + str(stamina) + '/' + str(percent_perfection) + '%'
                if nickname == new_name:
                	continue
                pokemon_count += 1
                api.nickname_pokemon(pokemon_id = poke_id, nickname = new_name)
                api.call()
                time.sleep(.5)
                print species_name + ' "' + nickname + '" renamed to "' + new_name + '"'
    print str(pokemon_count) + ' pokemon were modified.'

if __name__ == '__main__':
	main()
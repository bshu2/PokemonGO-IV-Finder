import time
import logging
import argparse
import getpass
from pgoapi import pgoapi

log = logging.getLogger(__name__)

def init_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')", required=True)
    parser.add_argument("-u", "--username", help="Username", required=True)
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-lat", "--latitude", help="Latitude", required=True)
    parser.add_argument("-long", "--longitude", help="Longitude", required=True)
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
                attack = pokemon['individual_attack']
                defense = pokemon['individual_defense']
                stamina = pokemon['individual_stamina']
                percent_perfection = int((float(attack + defense + stamina) / 45.0) * 100.0)

                new_name = str(attack) + '/' + str(defense) + '/' + str(stamina) + '/' + str(percent_perfection) + '%'
                pokemon_count += 1
                api.nickname_pokemon(pokemon_id = poke_id, nickname = new_name)
                api.call()
                time.sleep(1)
                print new_name
    print str(pokemon_count) + ' pokemon were modified.'
main()
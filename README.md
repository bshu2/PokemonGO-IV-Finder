# PokemonGO-IV-Finder
Gets the IV stats for Pokémon and renames them according to those stats.
For example, a Pikachu with IV stats of 12 Attack, 14 Defense, and 10 Stamina will be renamed to "12/14/10/80%"

Written in Python and uses [pgoapi](https://github.com/tejado/pgoapi) by [tjado](https://github.com/tejado)


## Installation
```
git clone https://github.com/bshu2/PokemonGO-IV-Finder.git
cd PokemonGO-IV-Finder
pip install git+https://github.com/tejado/pgoapi.git
```


## Usage
```
python ivfinder.py -a AUTH_SERVICE -u USERNAME [-p PASSWORD] -lat LATITUDE -long LONGITUDE [--reset]
```
AUTH_SERVICE must be either ptc or google

USERNAME is the username of the account you are logging in with

PASSWORD is the corresponding password to that username (if ommitted, you will be prompted to enter the password)

LATITUDE and LONGITUDE represent the location where you are to spawn

Include `--reset` to reset the names of all Pokemon to their original names
'''
Created on Jul 29, 2023

@author: ayan
'''
import requests
import pprint

# this is a test line
parameters = {
    "lat": 40.71,
    "lon": -74
}

resp = requests.get("https://pokeapi.co/api/v2/pokemon/charizard")
print(resp.json())
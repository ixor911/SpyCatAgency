import requests


"""
Get breeds from api
"""

breeds = {}
for breed in requests.get('https://api.thecatapi.com/v1/breeds').json():
    breeds[breed.get('id')] = breed


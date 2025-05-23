import requests

breeds = {}
for breed in requests.get('https://api.thecatapi.com/v1/breeds').json():
    breeds[breed.get('id')] = breed

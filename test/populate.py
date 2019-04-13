


import json
import requests
import pathlib



datasets = [str(x) for x in pathlib.glob('./datasets/*.json')]

for d in datasets:
    with f as open(d, 'r'):
        json_object = json.load(d)
        requests.post('http://localhost)


#! /bin/bash
cd .

curl -d @$(readlink -f './datasets/beverage_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/beverage
curl -d @$(readlink -f './datasets/flights_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/flights
curl -d @$(readlink -f ./datasets/lights_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/lights
echo "Done populating"

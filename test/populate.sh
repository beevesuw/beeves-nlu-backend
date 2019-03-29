#! /bin/bash
cd .
curl -d @./datasets/beverage_dataset.json  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/beverage
curl -d @./datasets/flights_dataset.json  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/flights
curl -d @./datasets/lights_dataset.json  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/lights
echo "Done populating"

#! /bin/bash

URL=${BEEVES_SERVER_URL:-localhost:8337}

if [[ "$#" -gt 0 ]]; then
    echo "Connecting to $URL"
    curl  -d "{\"q\" : \"$1\"}"   -v --request POST -H "Content-Type: application/json" --url localhost:8337/grok  --cookie "BEEVES_KEY=$BEEVES_KEY"
fi

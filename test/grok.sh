#! /bin/bash

URL=${BEEVES_SERVER_URL:-localhost:8337}

if [[ "$#" -gt 0 ]]; then
    echo "Connecting to $URL"
    curl  -d "{\"skill_name\" : \"$1\", \"text\" : \"$2\",  \"top_n\" : $3}"   -v --request POST -H "Content-Type: application/json" --url $URL/grok  --cookie "BEEVES_KEY=$BEEVES_KEY"
fi

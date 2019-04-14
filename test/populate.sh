#! /bin/bash
SCRIPTPATH=$(readlink -f $0)
SCRIPTDIR=`dirname $SCRIPTPATH`

URL=${BEEVES_SERVER_URL:-localhost:8337}

echo $SCRIPTDIR
echo $SCRIPTPATH

pushd $SCRIPTDIR

DBFILE="../skill_store.db"
if [ -f $DBFILE ]; then
   echo "The file '$DBFILE' exists."
   read -p "Remove and reupload skills? " -n 1 -r
   echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
    rm -f FILE
    echo "Removed '$DBFILE'"

    else
    exit
    fi
fi


echo "Populating to $URL"
curl -d @$(readlink -f './datasets/beverage_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url $URL/skill/beverage  --cookie "BEEVES_KEY=$BEEVES_KEY"
curl -d @$(readlink -f './datasets/flights_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url  $URL/skill/flights --cookie "BEEVES_KEY=$BEEVES_KEY"
curl -d @$(readlink -f './datasets/lights_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url  $URL/skill/lights --cookie "BEEVES_KEY=$BEEVES_KEY"
echo "Done populating to $URL"

popd

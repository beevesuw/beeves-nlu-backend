#! /bin/bash
SCRIPTPATH=$(readlink -f $0)
SCRIPTDIR=`dirname $SCRIPTPATH`

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

curl -d @$(readlink -f './datasets/beverage_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/beverage
curl -d @$(readlink -f './datasets/flights_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/flights
curl -d @$(readlink -f './datasets/lights_dataset.json')  -v --request PUT -H "Content-Type: application/json" --url http://localhost:5000/skill/lights
echo "Done populating"

popd

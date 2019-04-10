# beeves-nlu-backend

## Docker:

It's supposed to be something like this, but I haven't checkeed yet:

~~~
docker build -t bv-nlu .
docker exec -ti bv-nlu sh -c "export FLASK ENV=development;flask run -h 127.0.0.1 -p 5000" -v storage:storage

docker run -v storage:storage -t -i bv-nlu:latest bash

~~~

docker run -v name:/path/to/persist -t -i myimage:latest bash

## Run

Run the app:

~~~
export FLASK_ENV=development
flask run -h 127.0.0.1 -p 5000
~~~


## Test

Run `populate.sh` to load up the example datasets:

~~~
./test/populate.sh
~~~

This POSTs a bunch of skill definitions that live in `test/datasets`. These are SnipsNLUEngine specifications. We're going to change this immediately to generalize, but that's how it was for the demo, so I'm just restoring to that point.


# Endpoints

- `/`, `/skills`: list the skills

- `/grok`: POST a statement like  this via curl: `curl -d '{"q":"beverage make me coffee"}' -H "Content-Type: application/json" -X POST http://localhost:5000/grok` and you get the result of SnipsNLUEngine.parse
- `/skill/<skill_name>`: get the original skill def




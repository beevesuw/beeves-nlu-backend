# beeves-nlu-backend

## Docker:

Do this in the `beeves-nlu-backend` directory (make sure all your containers and images are cleaned and pruned):
~~~
docker build -t altanorhon/beeves:beeves-nlu-backend .

docker run --name bvn -v storage:/storage -p 8337:8337 altanorhon/beeves:beeves-nlu-backend -e "BEEVES_KEY=hunter2"
~~~

Where `BEEVES_KEY` is specified either as a cookie that all clients should send (with the key being `BEEVES_KEY` and the value `hunter2`)  or as a `GET` parameter (e.g., `localhost:8337/?beeves_key=hunter2`)

## Just Docker

# Instructions:

`docker run --name bvn -v storage:/storage -p 8337:8337 altanorhon/beeves:beeves-nlu-backend`


## Test

Note that the host is going to be localhost by default, and the port is going to be `8337 (BEEV, from 8 3 3 7 )`

However, by defining the `BEEVES_SERVER_URL` environment variable, you can set a custom URL for that script:

`export BEEVES_SERVER_URL=example.com:8337`

If you have set a `BEEVES_KEY`, you're going to want that too:

`export BEEVES_KEY=hunter2` 

Run `populate.sh` to load up the example datasets:

~~~
./test/populate.sh
~~~

This POSTs a bunch of skill definitions that live in `test/datasets`. These are SnipsNLUEngine specifications.

There is also `grok.sh`, which can be used like this:

~~~
./test/grok.sh "beverage make me tea"
~~~

# API Endpoints

- `/`, `/skills`, `/skill`: list the skills
- `/skill/<skill_name>`: get the original skill def
- `/grok`: POST a statement like  this via curl: `curl -d '{"q":"beverage make me coffee"}' -H "Content-Type: application/json" -X POST http://localhost:8337/grok` and you get the result of SnipsNLUEngine.parse




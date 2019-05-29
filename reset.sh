#!/bin/bash

#assuming the bvn image is built, this stops the container, removes it and runs it again
docker stop bvn 
docker rm bvn 
docker run --name bvn -v storage:/storage -p 8337:8337 altanorhon/beeves:beeves-nlu-backend

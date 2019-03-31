# Build an image that can do training and inference in SageMaker
# This is a Python 2 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM debian:stretch

MAINTAINER Altan Orhon <altan@uw.edu>


RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         python3-setuptools \
         python3-pip \
         ca-certificates



ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY . /opt/program
WORKDIR /opt/program




# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app


RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

RUN  run  # TODO: Figur eout


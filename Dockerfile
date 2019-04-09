FROM debian:stretch


LABEL summary="The beeeves NLU backend" \
  io.k8s.description="The beeves NLU backend" \
  name="beeves/beeves-nlu-backend" \
  version="0.0.3" \
  com.redhat.component="beeves-nlu-backend-docker" \
  maintainer="Altan Orhon <altan@uw.edu>"


RUN apt-get -y update && apt-get install -y --no-install-recommends \
  curl \
  python3 \
  python3-setuptools \
  python3-pip \
  python3-dev \
  build-essential \
  ca-certificates && apt-get clean

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY . /opt/program
WORKDIR /opt/program


EXPOSE 8337

# We copy just the requirements.txt first to leverage Docker cache

RUN pip3 install -r requirements.txt

# this stands for BEEV:
CMD ["/bin/bash"]

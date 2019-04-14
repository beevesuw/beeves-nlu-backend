# Instructions:
# docker build -t altanorhon/beeves:beeves-nlu-backend .
# docker run --name bvn -v storage:/storage -p 8337:8337 altanorhon/beeves:beeves-nlu-backend


FROM python:3.7.3-stretch

LABEL summary="The beeeves NLU backend" \
  io.k8s.description="The beeves NLU backend" \
  name="beeves/beeves-nlu-backend" \
  version="0.0.3" \
  com.redhat.component="beeves-nlu-backend-docker" \
  maintainer="Altan Orhon <altan@uw.edu>"


WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python3 -m snips_nlu download en

EXPOSE 8337

ENV FLASK_APP app
ENV FLASK_ENV development

# this stands for BEEV:
# ENTRYPOINT [ "python app" ]

# CMD ["flask run "]


ENTRYPOINT [ "python3", "bvapi/app.py"]

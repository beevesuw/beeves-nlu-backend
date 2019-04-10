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

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8337"]

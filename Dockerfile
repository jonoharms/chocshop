FROM python:3.12-bookworm

ENV FLASK_APP chocshop.py
ENV FLASK_CONFIG docker

RUN adduser -disabled-password --gecos "" chocshop
USER chocshop
WORKDIR /home/chocshop

# Create the environment:
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

#copy app
COPY app app
COPY migrations migrations
COPY chocshop.py config.py boot.sh ./

# runtime configuration
#RUN ["chmod", "+x", "./boot.sh"]
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

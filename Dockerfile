FROM python:3.7.7-alpine

ENV FLASK_APP chocshop.py
ENV FLASK_CONFIG docker

RUN adduser -D chocshop
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
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
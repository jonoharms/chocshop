FROM continuumio/anaconda3:2020.02-alpine

ENV FLASK_APP chocshop.py
ENV FLASK_CONFIG docker

#RUN useradd -D chocshop
RUN useradd -ms /bin/bash chocshop
USER chocshop

WORKDIR /home/chocshop

COPY environment.yml environment.yml
RUN conda env create -f environment.yml

COPY app app
COPY migrations migrations
COPY chocshop.py config.py boot.sh ./

# runtime configuration
EXPOSE 5001
ENTRYPOINT ["./boot.sh"]
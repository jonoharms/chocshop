FROM continuumio/anaconda3:2020.02-alpine

ENV FLASK_APP chocshop.py
ENV FLASK_CONFIG docker

USER anaconda
WORKDIR /home/anaconda

ENV PATH="/opt/conda/bin:${PATH}"


COPY environment.yml environment.yml
RUN conda env create -f environment.yml

COPY app app
COPY migrations migrations
COPY chocshop.py config.py boot.sh ./

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
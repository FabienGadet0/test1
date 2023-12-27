FROM postgres:latest

ENV POSTGRES_DB production
ENV POSTGRES_USER user
ENV POSTGRES_PASSWORD pwd

COPY ./queries/* /docker-entrypoint-initdb.d/

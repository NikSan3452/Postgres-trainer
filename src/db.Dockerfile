FROM postgres
ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB postgres 
COPY CreateDB.sql /docker-entrypoint-initdb.d/
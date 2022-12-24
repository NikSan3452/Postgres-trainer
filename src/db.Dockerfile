FROM postgres
ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB testdb 
COPY CreateDB.sql /docker-entrypoint-initdb.d/
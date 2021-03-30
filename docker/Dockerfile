FROM python:3.7-slim

# Instala dependencias
RUN apt update &&\
    apt install -y gcc pkg-config openssl libcurl4-openssl-dev libssl-dev \
                   build-essential libssl-dev  libffi-dev python3-dev \
                   unixodbc-dev postgresql postgresql-contrib

# Define novo diretorio de trabalho
WORKDIR /app

# Instala uWSGI
RUN pip3 install uwsgi

# Copia script de inicialização e variáveis de ambiente
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh

EXPOSE 3031
ENTRYPOINT [ "/entrypoint.sh" ]
ENV EXEC_ENV=DEV
CMD [ "uwsgi", "--socket", ":3031", "--wsgi-file", "/app/config/wsgi.py", "--master", "--processes", "4", "--threads", "2", "--stats", "/dev/stdout" ]

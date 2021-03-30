#!/bin/bash
set -e

if [[ "$EXEC_ENV" == "DEV" ]]; then
	pip3 install -r /app/requirements.txt
	export DEBUG_VAR="True"
#	python3 /app/manage.py migrate
fi

if [[ "$EXEC_ENV" == "PROD" ]]; then
	source /app.env
	if [[ -z $DB_USER ]] || [[ -z $DB_HOST ]] || [[ -z $DB_PASS  ]] || [[ -z $DB_BASE ]]; then
		echo "ERRO: dados para conexão com base de dados não informado. Abortando a aplicação.."
		exit 1
	fi
fi

exec "$@"

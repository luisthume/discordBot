#!/bin/sh
set -e

if [ -d /app ] && [ -f /app/requirements.txt ]; then
	echo '*** Encontrado: requirements.txt\nInstalando dependencias..'
	pip3 install -r /app/requirements.txt
	echo '*** Dependencias instaladas.'

	echo '*** Restaurando permissões do usuário www-data..'
	chown -R www-data:www-data /app
	echo '** Permissões restauradas.'
fi

#echo '*** Executando migrações.. ***'
#chmod +x /app/manage.py
#/app/manage.py migrate

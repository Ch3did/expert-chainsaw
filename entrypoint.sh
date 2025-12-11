#!/bin/sh

set -e

echo ">>> Run Migration"

until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Aguardando banco de dados $POSTGRES_HOST na porta $POSTGRES_PORT..."
  sleep 2
done

echo "Banco de dados online. Executando migrations..."
python3 manage.py migrate

exec "$@"

python3 manage.py migrate
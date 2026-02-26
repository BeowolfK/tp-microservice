#!/bin/bash
set -e

for db in product_db customer_db inventory_db pricing_db order_db; do
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $db;
EOSQL
done

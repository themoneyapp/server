#! /usr/bin/env bash

# Let the DB start
python /app/app/scripts/app_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/scripts/initial_data.py

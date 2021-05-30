#! /usr/bin/env bash
set -e

python /app/app/scripts/worker_pre_start.py

celery worker -A app.worker -l info -Q main-queue -c 1

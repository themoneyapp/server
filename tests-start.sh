#! /usr/bin/env bash
set -e

python /app/app/scripts/tests_pre_start.py

bash ./scripts/test.sh "$@"

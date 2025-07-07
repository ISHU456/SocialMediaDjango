#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create media directory if it doesn't exist
mkdir -p media

python manage.py collectstatic --no-input
python manage.py migrate 
#!/bin/bash
set -e
#pip install -r /app/requirements.txt
gunicorn -b 0.0.0.0:8000 app:api
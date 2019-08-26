#!/bin/bash
set -e
#pip install -r /app/requirements.txt
cd /app && gunicorn -b 0.0.0.0:8000 app:api
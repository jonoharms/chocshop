#!/bin/sh
conda activate ./venv
flask deploy
exec gunicorn -b 0.0.0.0:5001 --access-logfile - --error-logfile - chocshop:app
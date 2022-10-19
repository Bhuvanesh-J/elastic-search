#!/bin/bash
. venv/bin/activate
pip install -r requirements.txt
fuser -k 9000/tcp
nohup python app.py &


#!/bin/sh

export FLASK_APP=server
python3 -m flask run -h 0.0.0.0 -p 8080

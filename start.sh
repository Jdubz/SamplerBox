#!/bin/sh

export FLASK_APP=server/server
python3 -m flask run -h 0.0.0.0

#!/usr/bin/env python

from flask import Flask

import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

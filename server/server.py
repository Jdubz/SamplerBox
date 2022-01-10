#!/usr/bin/env python

from flask import Flask
import audio
import samples
import midi

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

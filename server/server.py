#!/usr/bin/env python3

from flask import Flask
import samplerbox

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

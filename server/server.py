#!/usr/bin/env python

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import sounddevice

# import sampler

app = Flask(__name__, static_folder='../build', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/audiodevice', methods=['GET'])
@cross_origin()
def audiodevice():
    devices = sounddevice.query_devices()
    return jsonify(devices)

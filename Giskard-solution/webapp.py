# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 22:35:54 2023

@author: nacha
"""


from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from Galaxy import *

import pandas as pd
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'json'}
INPUT_BACKEND = './millennium-falcon.json'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def compute_the_odds(input_frontend):
    Empire_json = pd.read_json(input_frontend, typ='series')
    empire = Empire(Empire_json.countdown, Empire_json.bounty_hunters)

    MF_json = pd.read_json(INPUT_BACKEND, typ='series') 
    millennium_falcon = Millennium_falcon(MF_json.autonomy, MF_json.departure, MF_json.arrival, MF_json.routes_db,
                                        empire.countdown, empire.bounty_hunters)
    result = Millennium_falcon.give_me_the_odds(millennium_falcon)
    odds = result[0]
    return odds

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/get_the_odds", methods=['POST'])
def get_me_the_odds():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'json' not in request.files:
            return "No file provider"
        file = request.files['json']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return "No file provided"
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        return str(compute_the_odds(filepath))


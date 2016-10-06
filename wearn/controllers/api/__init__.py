# Dependencies
import base64
import cPickle as pickle
import hashlib
import json
import random
import os

from flask import request
from wearn import app, flask
from wearn.encoders.json_encoder import JSONEncoder
from wearn.models.wear import Wear

@app.route('/api/v1/search', methods=['POST'])
def search():

    # Get file
    file = base64.b64decode(request.form['file'])
    filename = os.path.join(app.config['UPLOAD_FOLDER'], hashlib.sha224(file).hexdigest()) + '.jpg'
    with open(filename, 'wb') as f:
        f.write(file)

    # Calculate predictions
    predictions = Wear.search(filename)

    # Show best results by euclidean distance
    predictions_by_euclidean = sorted(predictions, key=lambda x: x[3])[:10]

    # Show best results by cosine distance
    # predictions_by_cosine = sorted(predictions, key=lambda x: x[4])[:10]

    # Show best results by correlation distance
    # predictions_by_correlation = sorted(predictions, key=lambda x: x[5])[:10]

    # TODO: encoding float with 6 decimal places
    for prediction in predictions_by_euclidean:
        del prediction[3]

    return json.dumps(predictions_by_euclidean)
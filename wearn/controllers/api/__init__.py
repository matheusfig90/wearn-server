# Dependencies
import cPickle as pickle
import json
import os

from flask import request
from wearn import app, flask
from wearn.encoders.json_encoder import JSONEncoder
from wearn.models.wear import Wear

@app.route('/api/v1/search', methods=['POST'])
def search():

    # Get file
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # Calculate predictions
    predictions = Wear.search(file.filename)

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
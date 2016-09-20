# Dependencies
from wearn import app, flask

@app.route('/demo', methods=['GET'])
def demo():
    return flask.render_template('demo.html')
from flask import render_template

from simplecms import app


@app.route('/god', methods=['GET'])
def god():
    return render_template('god.html')

from flask import (
    current_app,
    Blueprint,
    render_template
)

import requests

frontend = Blueprint('frontend', __name__, template_folder='templates')

headers = {"Content-type": "application/json"}

@frontend.route('/')
def index():
    premises_url = current_app.config['PREMISES_REGISTER']
    url = "%s/search?_query=&_representation=json" % premises_url
    resp = requests.get(url, headers=headers)
    current_app.logger.info(resp.json())
    return render_template('index.html', data=resp.json())

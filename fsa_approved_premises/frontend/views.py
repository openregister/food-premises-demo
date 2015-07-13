from flask import (
    current_app,
    Blueprint,
    render_template,
    request,
    jsonify
)

import requests

frontend = Blueprint('frontend', __name__, template_folder='templates')

headers = {"Content-type": "application/json"}


@frontend.route('/')
def index():
    premises_url = current_app.config['PREMISES_REGISTER']
    url = "%s/search?_representation=json" % premises_url
    resp = requests.get(url, headers=headers)
    return render_template('index.html', data=resp.json())

@frontend.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 0)
    premises_url = current_app.config['PREMISES_REGISTER']
    url = "%s/search?_query=%s&_page=%s&_representation=json" % (premises_url, query, page)
    resp = requests.get(url, headers=headers)
    current_app.logger.info(resp.json())
    return jsonify(resp.json())

from flask import (
    current_app,
    Blueprint,
    render_template,
    request,
    jsonify,
    abort
)


import requests

frontend = Blueprint('frontend', __name__, template_folder='templates')

headers = {"Content-type": "application/json"}

@frontend.route('/')
def index():
    premises_url = current_app.config['PREMISES_REGISTER']
    url = "%s/search?_representation=json" % premises_url
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        abort(resp.status_code)
    return render_template('index.html', data=resp.json())


@frontend.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 0)
    premises_url = current_app.config['PREMISES_REGISTER']
    url = "%s/search?_query=%s&_page=%s&_representation=json" % (premises_url, query, page)
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        abort(resp.status_code)
    current_app.logger.info(resp.json())
    return jsonify(resp.json())


@frontend.route('/premises/<int:id>')
def premises(id):
    premises_register = current_app.config['PREMISES_REGISTER']
    poao_premises_register = current_app.config['POAO_PREMISES_REGISTER']
    address_register = current_app.config['ADDRESS_REGISTER']
    try:
        premises_url = '%s/premises/%d.json' % (premises_register, id)
        resp = requests.get(premises_url, headers=headers)
        resp.raise_for_status()
        premises = resp.json()

        poao_premises_url = '%s/premises/%d.json' % (poao_premises_register, id)
        resp = requests.get(poao_premises_url, headers=headers)
        resp.raise_for_status()
        poao_premises = resp.json()

        address_url = '%s/address/%d.json' % (address_register, id)
        resp = requests.get(address_url, headers=headers)
        resp.raise_for_status()
        address = resp.json()

    except requests.exceptions.HTTPError as e:
        current_app.logger.info(e)
        abort(resp.status_code)
    return render_template('premises.html', poao_premises_register=poao_premises_register, premises=premises, poao_premises=poao_premises, address=address)

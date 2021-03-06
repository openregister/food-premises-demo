import collections
import jinja2
import requests

from flask import (
    current_app,
    Blueprint,
    render_template,
    request,
    jsonify,
    abort
)

frontend = Blueprint('frontend', __name__, template_folder='templates')

headers = {"Content-type": "application/json"}

@jinja2.contextfilter
@frontend.app_template_filter()
def format_link(context, value):
    items = value.split(':')
    register = current_app.config['POAO_SECTION_REGISTER']
    return "<a href='%s/products-of-animal-origin-section/%s'>%s</a> %s" % (register, items[0],items[0],items[1])


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
    food_category_register = current_app.config['FOOD_ESTABLISHMENT_CATEGORY_REGISTER']
    try:
        premises_url = '%s/premises/%d.json' % (premises_register, id)
        resp = requests.get(premises_url, headers=headers)
        resp.raise_for_status()
        premises = resp.json()

        poao_premises_url = '%s/premises/%d.json' % (poao_premises_register, id)
        resp = requests.get(poao_premises_url, headers=headers)
        resp.raise_for_status()
        poao_premises = resp.json()

        category_details = _get_category_details(poao_premises)

        address_url = '%s/address/%d.json' % (address_register, id)
        resp = requests.get(address_url, headers=headers)
        resp.raise_for_status()
        address = resp.json()

    except requests.exceptions.HTTPError as e:
        current_app.logger.info(e)
        abort(resp.status_code)
    return render_template('premises.html',
                           poao_premises_register=poao_premises_register,
                           premises=premises, poao_premises=poao_premises,
                           address=address,
                           category_details=category_details,
                           food_category_register=food_category_register)


Category = collections.namedtuple('Category', 'category_key, section_name, activity_name')


# This sort of stuff is a mess.
def _get_category_details(premises):
    category_details = []
    try:
        for category in premises['entry']['food-establishment-categories']:
            section_key, activity_key = category.split(':')
            section_url = "%s/products-of-animal-origin-section/%s.json" % (current_app.config['POAO_SECTION_REGISTER'], section_key)
            activity_url = "%s/products-of-animal-origin-activity/%s.json" % (current_app.config['POAO_ACTIVITY_REGISTER'], activity_key)

            section_resp = requests.get(section_url, headers=headers)
            activity_resp = requests.get(activity_url, headers=headers)

            section_resp.raise_for_status()
            activity_resp.raise_for_status()

            section = section_resp.json()['entry']
            activity = activity_resp.json()['entry']
            category = Category(category_key=category,
                                section_name=section['name'],
                                activity_name=activity['name'])
            category_details.append(category)
        current_app.logger.info(category_details)

    except requests.exceptions.HTTPError as e:
        current_app.logger.info(e)
        current_app.logger.info('Not much we can do at this point but return empty category_details')

    return category_details


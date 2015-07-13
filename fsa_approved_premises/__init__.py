import os
from fsa_approved_premises.factory import create_app
app = create_app(os.environ['SETTINGS'])

from flask import Flask
from jinjax import Catalog


app = Flask(__name__)
app.jinja_env.auto_reload = True

import jinja2
enhanced_loader = jinja2.ChoiceLoader([
    jinja2.PackageLoader("py_flowbite_jinja_htmx", ""),
    app.jinja_loader
])

app.jinja_loader = enhanced_loader

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = '35d092ab79d654448e9041683b53975d8d432cad82ebd009'


# configure JinjaX with the Flask Jinja globals, filters, etc., like `url_for()`
catalog = Catalog(jinja_env=app.jinja_env)
catalog.add_folder("demo_app/templates/components")


import demo_app.webapp
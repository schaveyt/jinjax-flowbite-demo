import os
from flask import Flask
from jinjax import Catalog

import logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger('jinjax').setLevel(logging.DEBUG)


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

# add jinjax-flowbite components
JINJAX_FLOWBITE_DEV_ENV = os.environ.get("JINJAX_FLOWBITE_DEV")
if JINJAX_FLOWBITE_DEV_ENV is not None and JINJAX_FLOWBITE_DEV_ENV == "1":
    catalog.add_folder("../jinjax-flowbite/src/jinjax-flowbite/components", prefix="Flowbite")
else:
    import jinjax_flowbite
    catalog.add_module(jinjax_flowbite.components_path, prefix="Flowbite")

# add local jinjax components
catalog.add_folder("demo_app/jinjax_components")



import demo_app.webapp
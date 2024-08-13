import os
from flask import Flask
from jinjax import Catalog

# import logging
# logging.basicConfig(level=logging.WARNING)
# logging.getLogger('jinjax').setLevel(logging.DEBUG)


app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = '35d092ab79d654448e9041683b53975d8d432cad82ebd009'


# configure JinjaX with the Flask Jinja globals, filters, etc., like `url_for()`
jinjax_catalog = Catalog(jinja_env=app.jinja_env)

# add jinjax-flowbite components
JINJAX_FLOWBITE_DEV_ENV = os.environ.get("JINJAX_FLOWBITE_DEV")
if JINJAX_FLOWBITE_DEV_ENV is not None and JINJAX_FLOWBITE_DEV_ENV == "1":
    jinjax_catalog.add_folder("../jinjax-flowbite/src/jinjax-flowbite/components", prefix="Flowbite")
else:
    import jinjax_flowbite
    jinjax_catalog.add_module(jinjax_flowbite.components_path, prefix="Flowbite")

# add local jinjax components
jinjax_catalog.add_folder("demo_app/components")



import demo_app.webapp
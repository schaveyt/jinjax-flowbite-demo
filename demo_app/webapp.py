import os
import traceback
from flask import flash, render_template
from demo_app import app, jinjax_catalog
from demo_app.services.app_services import ApplicationServices


APP_VERSION = "v9.9.9"

# FOR DESKTOP APP ONLY
# if a win_exe_version_info.py exist, then we want to read the app version from the file.
#
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, "win_exe_version_info.py")
config_file = os.path.abspath(config_file)
if os.path.isfile(config_file):
    with open(config_file) as f:
        for _, line in enumerate(f):
            if "ProductVersion" in line:
                sanitized_line = line.strip().replace("StringStruct('ProductVersion', '", "")
                sanitized_line = sanitized_line.replace("'),", "")
                APP_VERSION = sanitized_line


app_services: ApplicationServices = ApplicationServices("JinjaX Flowbite Demo App", APP_VERSION)


if app.debug == True:
    print("dbg: detected app in debug mode.")
else:
    print("dbg: not in debug mode")

# import the page handlers
#
import demo_app.routes.index
import demo_app.routes.admin
import demo_app.routes.scc
import demo_app.routes.home
import demo_app.routes.counter
import demo_app.routes.fetch







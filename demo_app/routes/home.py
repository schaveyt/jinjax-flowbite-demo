import os
from flask import Response, flash, redirect, request, render_template
from demo_app.webapp import APP_VERSION, app_services, app, jinjax_catalog
from demo_app.routes.htmx_utils import htmx_redirect
import time

@app.route("/home")
def home_page() -> Response | str:
	
    using_mock = "mock" in str(type(app_services.auth_service)).lower()
    if not app_services.auth_service.is_authenticated and not using_mock:
        return htmx_redirect(request, "/")
    
    scc_fetch = request.args.get('scc_fetch')
    if scc_fetch:
        app_services.scc_service.fetch()
        return htmx_redirect(request, "/home")
    
    page_title = "Home"
    
    return jinjax_catalog.render("Pages.HomePage", app_services=app_services, page_title=page_title)


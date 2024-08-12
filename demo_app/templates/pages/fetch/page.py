import os
from flask import Response, flash, redirect, request, render_template
from demo_app.webapp import APP_VERSION, app_services, app
from demo_app.templates.htmx_utils import htmx_redirect
import time

@app.route("/fetch")
def fetch_page() -> Response | str:
	
    using_mock = "mock" in str(type(app_services.auth_service)).lower()
    if not app_services.auth_service.is_authenticated and not using_mock:
        return htmx_redirect(request, "/")
    
    scc_fetch = request.args.get('scc_fetch')
    if scc_fetch:
        app_services.scc_service.fetch()
        return htmx_redirect(request, "/fetch")
    
    page_title = "Fetch"
    
    return render_template("pages/fetch/page.html", app_services=app_services, page_title=page_title)


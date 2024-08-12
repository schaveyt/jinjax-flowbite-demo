import os
from flask import Response, redirect, render_template, request, url_for, flash
from demo_app.templates.htmx_utils import htmx_redirect
from demo_app.webapp import app_services, app



@app.route("/admin")
def admin_page() -> Response | str:

    scc_fetch = request.args.get('scc_fetch')
    if scc_fetch:
        app_services.scc_service.fetch()
        return htmx_redirect(request, "/admin")
    
    return render_template("pages/admin/page.html",
            app_services=app_services,
            page_title="Admin")





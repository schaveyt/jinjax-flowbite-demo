from flask import Response, request
from demo_app.routes.htmx_utils import htmx_redirect
from demo_app.webapp import app_services, app, jinjax_catalog

@app.route("/admin")
def admin_page() -> Response | str:

    scc_fetch = request.args.get('scc_fetch')
    if scc_fetch:
        app_services.scc_service.fetch()
        return htmx_redirect(request, "/admin")
    
    return jinjax_catalog.render("Pages.AdminPage", app_services=app_services, request=request)





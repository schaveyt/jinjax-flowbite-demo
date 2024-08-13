from flask import Response, request
from demo_app.webapp import app_services, app, jinjax_catalog
from demo_app.routes.htmx_utils import htmx_redirect

@app.route("/counter")
def counter_page() -> Response | str:
	
    using_mock = "mock" in str(type(app_services.auth_service)).lower()
    if not app_services.auth_service.is_authenticated and not using_mock:
        return htmx_redirect(request, "/")
    
    scc_fetch = request.args.get('scc_fetch')
    if scc_fetch:
        app_services.scc_service.fetch()
        return htmx_redirect(request, "/counter")

    
    return jinjax_catalog.render("Pages.CounterPage", app_services=app_services, request=request)


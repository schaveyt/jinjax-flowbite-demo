import os
import time
from flask import Response, redirect, render_template, request, url_for, flash
import webview
from demo_app.domain.result import Result
from demo_app.routes.htmx_utils import htmx_redirect
from demo_app.webapp import app_services, app, jinjax_catalog

@app.route("/", methods=('GET', 'POST'))
def index_page() -> Response | str:

    page_title="Login"

    if (app_services.app_state.app_error is not None):
        flash(app_services.app_state.app_error, "error")
    else:
        scc_fetch = request.args.get('scc_fetch')
        if scc_fetch:
            app_services.scc_service.fetch()
            return htmx_redirect(request, "/")
        
        if request.method == 'POST':

            username = request.form['username']
            password = request.form['password']
            
            if not username:
                flash('Username is required!', "error")
            elif not password:
                flash('Password is required!', "error")
            else:
                return login_and_redirect(username, password)

        if app_services.auth_service.is_authenticated:
            return htmx_redirect(request, "/home")
            
    if 'HX_REQUEST' in request.headers:
        return htmx_redirect(request, "/")
    
    return jinjax_catalog.render("Pages.IndexPage", app_services=app_services, page_title=page_title, request=request)


def login_and_redirect(username: str, password: str) -> Response | str:
    
    result = app_services.auth_service.login(username, password)

    if result.is_failed:
        flash(result.error, "error")
        return htmx_redirect(request, "/")
    
    return htmx_redirect(request, "/home")


@app.route("/logout")
def logout_page() -> Response | str:

    app_services.auth_service.logout()
    app_services.app_state.reset()
    return htmx_redirect(request, "/")



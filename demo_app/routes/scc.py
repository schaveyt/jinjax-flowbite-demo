from flask import Response, render_template, request, flash
from demo_app.routes.htmx_utils import htmx_redirect
from demo_app.webapp import app_services, app, jinjax_catalog



@app.route("/scc")
def scc_page() -> Response | str:

    scc_fetch = request.args.get('scc_fetch')
    if scc_fetch:
        app_services.scc_service.fetch()
        return htmx_redirect(request, "/scc")

    return jinjax_catalog.render("Pages.SourceControlPage", app_services=app_services)



@app.route("/scc/changes")
def scc_page_changes_htmx() -> Response | str:
    return jinjax_catalog.render("SourceControl.Changes", app_services=app_services)



@app.route("/scc/fetch")
def scc_page_fetch_htmx() -> Response | str:
    app_services.scc_service.fetch()
    return htmx_redirect(request, "/scc")




@app.route("/scc/sync")
def scc_page_sync_htmx() -> Response | str:
    result = app_services.scc_service.pull()
    if result.is_failed:
        flash(result.error, "error")

    result = app_services.scc_service.push()
    if result.is_failed:
        flash(result.error, "error")

    return htmx_redirect(request, "/scc")



@app.route("/scc/discard")
def scc_page_discard_htmx() -> Response | str:
    filepath = request.args.get('filepath')
    if filepath:
        result = app_services.scc_service.discard_items([filepath])
        if result.is_failed:
            flash(result.error, "error")
    return htmx_redirect(request, "/scc")




@app.route("/scc/stage")
def scc_page_stage_htmx() -> Response | str:
    filepath = request.args.get('filepath')
    if filepath:
        result = app_services.scc_service.stage_items([filepath])
        if result.is_failed:
            flash(result.error, "error")
    return htmx_redirect(request, "/scc")




@app.route("/scc/unstage")
def scc_page_unstage_htmx() -> Response | str:
    filepath = request.args.get('filepath')
    if filepath:
        result = app_services.scc_service.unstage_items([filepath])
        if result.is_failed:
            flash(result.error, "error")
    return htmx_redirect(request, "/scc")




@app.route("/scc/commit", methods=('GET', 'POST'))
def scc_page_commit_htmx() -> Response | str:
    
    if request.method == 'POST':

        commit_msg = request.form['commit_msg']
       
        if not commit_msg:
            flash('A commit message is required!', "error")
        elif len(commit_msg) == 0:
            flash('A commit message is required!', "error")
        else:
            app_services.app_state.pending_commit_msg = commit_msg
            result = app_services.scc_service.commit(commit_msg)
            if result.is_failed:
                flash(result.error, "error")
            else:
                app_services.app_state.pending_commit_msg = ""
        
    return htmx_redirect(request, "/scc")




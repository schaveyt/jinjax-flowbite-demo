from flask import Request, Response, redirect

def htmx_redirect(request: Request, url: str) -> Response:
    if 'HX_REQUEST' in request.headers:
        response = Response()
        response.headers["hx-redirect"] = url
        return response
    return redirect("/")

        
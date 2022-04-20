from bottle import get, view, request, redirect, response
import g

@get("/sign-in")
@view("index")
def _():
    is_xhr = True if request.headers.get("spa") else False
    if is_xhr:
        return sign_in_as_module()

    if g.IS_VALID_SESSION():
        return redirect("/home")
    return dict(is_xhr = is_xhr, modal = "modals/sign_in", page_title = "Sign-in")

@view("modals/sign_in")
def sign_in_as_module():
    return
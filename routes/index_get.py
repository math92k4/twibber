from bottle import get, view, request, redirect
import g

##############################

@get("/")
@view("index")
def _():
    is_xhr = True if request.headers.get("spa") else False
    if g.IS_VALID_SESSION() and not is_xhr:
        return redirect("/home")
    return dict(is_xhr = is_xhr, modal = False, page_title = "Welcome to Twibber")
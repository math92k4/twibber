from bottle import get, view, request, redirect
import g

##############################

@get("/sign-up")
@view("index")
def _():
    is_xhr = True if request.headers.get("spa") else False
    if is_xhr:
        return sign_up_as_module()
    
    if g.IS_VALID_SESSION():
        return redirect("/home")

    return dict(is_xhr = is_xhr, modal = "modals/sign_up", page_title = "Sign-in")


##############################

@view("modals/sign_up")
def sign_up_as_module():
    return
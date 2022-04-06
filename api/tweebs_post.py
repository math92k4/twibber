from bottle import post, request

##############################

@post("/tweebs")
def _():
    tweeb_text = request.forms.get("tweeb_text")
    
    return tweeb_text

##############################
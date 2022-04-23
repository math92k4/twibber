from bottle import get, static_file

##############################

@get("/assets/<dir_name>/<file_name>")
def _(dir_name, file_name):
    return static_file(file_name, root=f"./assets/{dir_name}")

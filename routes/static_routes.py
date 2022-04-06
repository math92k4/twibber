from bottle import get, static_file

##############################

@get("/assets/<dir_name>/<file_name>")
def _(dir_name, file_name):
    print(f"./assets/{dir_name}")
    return static_file(file_name, root=f"./assets/{dir_name}")


##############################

@get("/assets/icons/<dir_name>/<file_name>")
def _(dir_name, file_name):
    print("#"*30)
    print(f"./assets/{dir_name}")
    return static_file(file_name, root=f"./assets/icons{dir_name}")
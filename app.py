from bottle import get, view, run, redirect, request, post
import pymysql
import g

##############################

import routes.static_routes

# API's
import api.tweebs_post
import api.users_post
import api.sessions_post

##############################

def get_tweebs():
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE fk_user_id = user_id""")
        tweebs = cursor.fetchall()
        return tweebs
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        db.close()


##############################

@get("/")
@view("index")
def _():
    is_xhr = True if request.headers.get("spa") else False
    if g.IS_VALID_SESSION() and not is_xhr:
        return redirect("/home")
    return dict(is_xhr = is_xhr, modal = False, page_title = "Welcome to Twibber")

##############################

@get("/sign-up")
@view("index")
def _():
    is_xhr = True if request.headers.get("spa") else False
    return dict(is_xhr = is_xhr, modal = "modals/sign_up", page_title = "Sign-in")

##############################

@get("/sign-in")
@view("index")
def _():
    is_xhr = True if request.headers.get("spa") else False
    return dict(is_xhr = is_xhr, modal = "modals/sign_in", page_title = "Sign-in")

##############################

@get("/home")
@view("main")
def _():
    tweebs = get_tweebs()
    is_xhr = True if request.headers.get("spa") else False
    return dict(is_xhr = is_xhr, tweebs = tweebs, spa_url = "/home")

##############################



@get("/<user_tag>")
@view("main")
def _(user_tag):
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM tweebs
                    JOIN users
                    WHERE fk_user_id = user_id AND user_tag = %s""", (user_tag,))
        tweebs = cursor.fetchall()

        is_xhr = True if request.headers.get("spa") else False
        return dict(is_xhr = is_xhr, tweebs = tweebs, spa_url = f"/{user_tag}")


    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        db.close()



##############################

@get("/compose/tweeb")
@get("/main")
def _():
    is_xhr = True if request.headers.get("spa") else False
    if is_xhr: 
        return create_tweeb_as_modal()

    if not g.IS_VALID_SESSION():
        return redirect("/")

    return dict(is_xhr = False, spa_url = "/home", modal = "modals/create_tweeb", tweebs = {})

@view("modals/create_tweeb")
def create_tweeb_as_modal(): 
    return

##############################



run( host="127.0.0.1", port=5555, debug=True, reloader=True )
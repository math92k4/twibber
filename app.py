from bottle import get, view, run, redirect, request, post, response
import pymysql
import g
import json

##############################

# Routes
import routes.static_routes
import routes.sign_out_get

# API's
import api.tweebs_post
import api.users_post
import api.sessions_post
import api.get_user_by_email
import api.tweebs_delete_by_id
import api.follows_post
import api.follows_delete
import api.tweebs_put

##############################
##############################
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
    if is_xhr:
        return sign_up_as_module()
    
    if g.IS_VALID_SESSION():
        return redirect("/home")

    return dict(is_xhr = is_xhr, modal = "modals/sign_up", page_title = "Sign-in")


@view("modals/sign_up")
def sign_up_as_module():
    return

##############################

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

##############################

# All tweets from user + those the user follows
@get("/home")
@view("main")
def _():
    is_xhr = True if request.headers.get("spa") else False

    if is_xhr and not g.IS_VALID_SESSION(is_xhr):
        return json.dumps({"error_url" : "/sign-out"})

    elif not g.IS_VALID_SESSION():
        return redirect("/explore")
    
    session = g.GET_DECODED_JWT()

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Check if follows someone
        cursor.execute("""SELECT * FROM follows
                        WHERE follower_id = %s""", (session["user_id"]),)
        followers = cursor.fetchall()

        if followers:
            # SELECTS all tweets from user + those accounts the user follow
            cursor.execute("""SELECT * FROM tweebs
                            JOIN users
                            JOIN follows
                            WHERE fk_user_id = following_id
                            AND follower_id = %s 
                            AND user_id = following_id
                            ORDER BY tweeb_created_at DESC""", (session["user_id"],))
            tweebs = cursor.fetchall()
            
        else:
            # SELECTS all tweets from user + those accounts the user follow
            cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE fk_user_id = user_id AND fk_user_id = %s
                        ORDER BY tweeb_created_at DESC""", (session["user_id"],))
            tweebs = cursor.fetchall()



        

        return dict(
            is_xhr = is_xhr, 
            tweebs = tweebs,
            modules = {"compose_tweet"},
            session = session,
            spa_url = "/home",
            page_title = "Home / Twibber",
            feed_title = "Home"
            )

    except Exception as ex:
        print(ex)

    finally:
        cursor.close()
        db.close()

##############################

# All tweets but the users
@get("/explore")
@view("main")
def _():
    print("explore")
    is_xhr = True if request.headers.get("spa") else False
    session = g.GET_DECODED_JWT()

    if not session:
        user_id = 0
    else: 
        user_id = session["user_id"]
    
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE fk_user_id = user_id AND fk_user_id != %s
                        ORDER BY tweeb_created_at DESC""", (user_id,))
        tweebs = cursor.fetchall()
        return dict(
            is_xhr = is_xhr, 
            tweebs = tweebs,
            modules = {},
            session = session, 
            spa_url = "/explore",
            page_title = "Explore / Twibber",
            feed_title = "Explore"
            )

    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        db.close()



##############################


# All tweets from specific user
@get("/<user_tag>")
@view("main")
def _(user_tag):
    is_xhr = True if request.headers.get("spa") else False
    session = g.GET_DECODED_JWT()

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Is user in db?
        cursor.execute("""SELECT * FROM users
                        WHERE user_tag = %s""", (user_tag,))
        user = cursor.fetchone()

        # Get user tweebs
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE fk_user_id = user_id 
                        AND user_tag = %s
                        ORDER BY tweeb_created_at DESC""", (user_tag,))
        tweebs = cursor.fetchall()

        # If has session and other user exist - see if follows
        is_following = False
        if session and user:
            follower_id = session["user_id"]
            following_id = user["user_id"]
            cursor.execute("""SELECT * FROM follows
                            WHERE follower_id = %s 
                            AND following_id = %s""", (follower_id, following_id))
            if cursor.fetchone():
                is_following = True

        # Generate page titles
        if user:
            feed_title = f"{user['user_first_name']} {user['user_last_name']}"
            page_title = f"{user['user_first_name']} {user['user_last_name']} (@{user['user_tag']}) / Twibber"
        else:
            feed_title = "Profile"
            page_title = "Profile / Twibber"

        return dict(
            is_xhr = is_xhr,
            tweebs = tweebs,
            modules = {"profile_section"},
            user = user,
            is_following = is_following,
            session = session, 
            spa_url = f"/{user_tag}",
            page_title = page_title,
            feed_title = feed_title
            )


    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        db.close()



##############################

@get("/compose/tweeb")
@get("/main")
def _():
    print("Compose")
    is_xhr = True if request.headers.get("spa") else False
    if is_xhr: 
        return create_tweeb_as_module()

    if not g.IS_VALID_SESSION():
        return redirect("/")

    return dict(is_xhr = is_xhr, spa_url = "/home", modal = "modals/create_tweeb", tweebs = {})

@view("modals/create_tweeb")
def create_tweeb_as_module():
    if not g.IS_VALID_SESSION(True):
        return {"error_url" : "/sign-out"}
    return dict(session = g.GET_DECODED_JWT())

##############################


@get("/update/<tweeb_id>")
@view("modals/update_tweeb")
def _(tweeb_id):
    is_xhr = True if request.headers.get("spa") else False
    if not is_xhr: 
        return redirect("/home")

    if not g.IS_VALID_SESSION(True):
        response.status = 400
        return { "error_url" : "/sign-out" }
    
    session = g.GET_DECODED_JWT()
    user_id = session["user_id"]

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE tweeb_id = %s
                        AND fk_user_id = user_id
                        AND user_id = %s""", (tweeb_id, user_id))
        tweeb = cursor.fetchone()

        if not tweeb:
            response.status = 204
            return

        return dict(tweeb = tweeb)
    
    except Exception as ex:
        print(ex)
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()



run( host="127.0.0.1", port=5555, debug=True, reloader=True )
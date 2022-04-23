from bottle import get, view, request, redirect, response
import g
import json
import pymysql

# All tweets from user + those the user follows
@get("/compose/tweeb")
@view("main")
def _():
    is_xhr = True if request.headers.get("spa") else False

    #VALIDATE SESSION
    if is_xhr:
        if not g.IS_VALID_SESSION(is_xhr):
            return json.dumps({"error_url" : "/sign-out"})
        return create_tweeb_as_module()

    elif not g.IS_VALID_SESSION():
        return redirect("/explore")
    
    session = g.GET_DECODED_JWT()

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # SELECTS all from accounts the user follows
        cursor.execute("""SELECT tweeb_id, tweeb_text, tweeb_image, tweeb_created_at, tweeb_updated_at, fk_user_id, user_first_name, user_last_name, user_tag, user_verified, user_icon_image
                        FROM tweebs
                        JOIN users
                        JOIN follows
                        WHERE fk_user_id = following_id
                        AND follower_id = %s
                        AND user_id = following_id
                        UNION
                        SELECT tweeb_id, tweeb_text, tweeb_image, tweeb_created_at, tweeb_updated_at, fk_user_id, user_first_name, user_last_name, user_tag, user_verified, user_icon_image
                        FROM tweebs
                        JOIN users
                        WHERE user_id = fk_user_id AND user_id = %s
                        ORDER BY tweeb_created_at DESC
                        LIMIT 25""", (session["user_id"], session["user_id"]))
        tweebs = cursor.fetchall()
            
        return dict(
            is_xhr = is_xhr,
            spa_url = "/home",
            feed_title = "Home",
            modules = {"compose_tweet"},
            page_title = "Compose tweeb",
            modal = "modals/compose_tweeb",
            session = session,
            tweebs = tweebs
            )

    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()


##############################

@view("modals/compose_tweeb")
def create_tweeb_as_module():
    return dict(session = g.GET_DECODED_JWT())
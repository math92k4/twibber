from itertools import count
from bottle import delete, response, request
import pymysql
import g

##############################

@delete("/follows")
def _():
    if not g.IS_VALID_SESSION():
        response.status = 400
        return { "error_url" : "/sign-out" }

    session = g.GET_DECODED_JWT()
    follower_id = session["user_id"]

    following_id = request.forms.get("user_id")
    if not following_id:
        response.status = 400
        return "No following id"

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        cursor.execute("""DELETE FROM follows
                        WHERE follower_id = %s 
                        AND following_id = %s""", (follower_id, following_id))
        count = cursor.rowcount
        db.commit()

        if not count:
            response.status = 204
            return

        # SUCCES
        response.status = 200
        return "User unfollowed"

    except Exception as ex:
        print(ex)
        response.status = 500
        return

    finally:
        cursor.close()
        db.close()
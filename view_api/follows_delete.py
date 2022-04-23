from itertools import count
from bottle import delete, response, request
import pymysql
import g

##############################

@delete("/follows")
def _():
    # VALIDATE DATA FROM CLIENT
    try:
        # Session
        if not g.IS_VALID_SESSION():
            response.status = 400
            return { "error_url" : "/sign-out" }
        session = g.GET_DECODED_JWT()
        follower_id = session["user_id"]

        # Following_id
        following_id = request.forms.get("user_id")
        if not g.IS_VALID_SERIAL(following_id):
            response.status = 400
            return { "error_url" : "/sign-out" }

    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return { "info" : "Server error" } 

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # DELETE follow
        cursor.execute("""DELETE FROM follows
                        WHERE follower_id = %s 
                        AND following_id = %s""", (follower_id, following_id))
        count = cursor.rowcount

        # No rows deleted
        if not count:
            response.status = 204
            return

        # UPDATE user_following on follower_id
        cursor.execute("""UPDATE users
                        SET user_following = user_following - 1
                        WHERE user_id = %s""", (follower_id,))

        # UPDATE user_followers on following_id
        cursor.execute("""UPDATE users
                        SET user_followers = user_followers - 1
                        WHERE user_id = %s""", (following_id,))
        db.commit()

        # SUCCES - row deleted
        response.status = 200
        return {"info" : "User unfollowed" }

    except Exception as ex:
        db.rollback()
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error" }

    finally:
        cursor.close()
        db.close()
from bottle import delete, response
import g
import pymysql
import os

##############################

@delete("/tweebs/<tweeb_id>")
def _(tweeb_id):
    # VALIDATE DATA FROM CLIENT
    try:
        if not g.IS_VALID_SESSION(True):
            response.status = 400
            return {"error_url" : "/sign-out"}
        session = g.GET_DECODED_JWT()

        if not g.IS_VALID_SERIAL(tweeb_id):
            response.status = 204
            return
    
    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error" }


    # CONNECT TO DB
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # try SELECT tweeb image
        cursor.execute("""SELECT tweeb_image FROM tweebs
                        WHERE tweeb_id = %s AND fk_user_id = %s
                        LIMIT 1""", (tweeb_id, session["user_id"]))
        tweeb_image = cursor.fetchone()
        if tweeb_image:
            tweeb_image = tweeb_image["tweeb_image"]

        # Delete the tweeb
        cursor.execute("""DELETE FROM tweebs
                        WHERE tweeb_id = %s AND fk_user_id = %s""", (tweeb_id, session["user_id"]))
        count = cursor.rowcount

        # No tweeb found / deleted
        if not count:
            response.status = 204
            return
        
        # UPDATE user_tweebs
        cursor.execute("""UPDATE users
                        SET user_tweebs = user_tweebs - 1
                        WHERE user_id = %s""", (session["user_id"],))
        db.commit()
        
        # if image - delete from server
        if tweeb_image:
            os.remove(f"assets/images/{tweeb_image}")

        response.status = 200
        return {"info" : f"Tweet with id: {tweeb_id} deleted"}

    except Exception as ex:
        db.rollback()
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error" }


    finally:
        cursor.close()
        db.close()

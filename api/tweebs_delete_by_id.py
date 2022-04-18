from bottle import delete, response
import g
import pymysql
import os

##############################

@delete("/tweebs/<tweeb_id>")
def _(tweeb_id):

    # VALIDATE
    if not g.IS_VALID_SESSION(True):
        response.status = 400
        return {"error_url" : "/sign-out"}
    
    session = g.GET_DECODED_JWT()

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Get tweeb image
        cursor.execute("""SELECT tweeb_image FROM tweebs
                        WHERE tweeb_id = %s AND fk_user_id = %s""", (tweeb_id, session["user_id"]))
        tweeb_image = cursor.fetchone()
        if tweeb_image:
            tweeb_image = tweeb_image["tweeb_image"]

        # Delete the tweeb
        cursor.execute("""DELETE FROM tweebs
                        WHERE tweeb_id = %s AND fk_user_id = %s""", (tweeb_id, session["user_id"]))
        count = cursor.rowcount
        db.commit()

        # No tweeb found / deleted
        if not count:
            response.status = 204
            return
        
        # if imgae - delete from server
        if tweeb_image:
            os.remove(f"assets/images/{tweeb_image}")

        response.status = 200
        return {"info" : f"Tweet with id: {tweeb_id} deleted"}

    except Exception as ex:
        print(ex)
        response.status = 500
        return 

    finally:
        return

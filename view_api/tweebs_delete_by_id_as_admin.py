from bottle import delete, response
import g
import pymysql
import os

##############################

@delete("/tweebs/<tweeb_id>/as-admin")
def _(tweeb_id):
    # VALIDATE DATA FROM CLIENT
    if not g.IS_VALID_SERIAL(tweeb_id):
        response.status = 204
        return

    # CONNECT TO DB
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # SELECT tweeb
        cursor.execute("""SELECT * FROM tweebs
                        WHERE tweeb_id = %s
                        LIMIT 1""", (tweeb_id,))
        tweeb = cursor.fetchone()

        # No tweeb found 
        if not tweeb:
            response.status = 204
            return

        # Extract image name if exist
        tweeb_image = False
        if tweeb["tweeb_image"]:
            tweeb_image = tweeb["tweeb_image"]

        # Delete the tweeb
        cursor.execute("""DELETE FROM tweebs
                        WHERE tweeb_id = %s""", (tweeb_id,))
        
        # UPDATE user_tweebs
        cursor.execute("""UPDATE users
                        SET user_tweebs = user_tweebs - 1
                        WHERE user_id = %s""", (tweeb["fk_user_id"],))
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

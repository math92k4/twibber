from bottle import post, response, request
import g
import pymysql

##############################

@post("/follows")
def _():
    if not g.IS_VALID_SESSION(True):
        response.status = 400
        return { "error_url" : "/sign-out" }

    session = g.GET_DECODED_JWT()
    follower_id = session["user_id"]

    following_id = request.forms.get("user_id")
    if not following_id:
        response.status = 400
        return "No user_id to follow"



    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM users
                        WHERE user_id = %s""", follower_id)
        if not cursor.fetchone():
            response.status = 400
            return "The user id doesn't exist"

        cursor.execute("""INSERT INTO follows (follower_id, following_id)
                        VALUES (%s, %s)""", (follower_id, following_id))
        db.commit()

        response.status = 200
        return "New follow created"
    
    except Exception as ex:
        if "Duplicate entry" in str(ex):
            response.status = 400
            return "You already follow this users"
        print(str(ex))
        response.status = 500
        return "Server error"
    
    finally:
        cursor.close()
        db.close()

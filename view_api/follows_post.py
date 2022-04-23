from bottle import post, response, request
import g
import pymysql

##############################

@post("/follows")
def _():
    # VALIDATE DATA FROM CLIENT
    try:
        # Session
        if not g.IS_VALID_SESSION(True):
            response.status = 400
            return { "error_url" : "/sign-out" }
        session = g.GET_DECODED_JWT()
        follower_id = session["user_id"]

        # Following id
        following_id = request.forms.get("user_id")
        if not g.IS_VALID_SERIAL(following_id):
            response.status = 400
            return { "error_url" : "/home" }

    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error" }
        
    # CONNECT TO DB
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # VALIDATE folliwing_id exist in db
        cursor.execute("""SELECT user_id FROM users
                        WHERE user_id = %s
                        LIMIT 1""", follower_id)
        user = cursor.fetchone()
        if not user:
            response.status = 400
            return { "error_url" : "/home" }


        # INSERT follow
        cursor.execute("""INSERT INTO follows (follower_id, following_id)
                        VALUES (%s, %s)""", (follower_id, following_id))

        # UPDATE user_following on follower_id
        cursor.execute("""UPDATE users
                        SET user_following = user_following + 1
                        WHERE user_id = %s""", (follower_id,))

        # UPDATE user_followers on following_id
        cursor.execute("""UPDATE users
                        SET user_followers = user_followers + 1
                        WHERE user_id = %s""", (following_id,))
        db.commit()

        response.status = 200
        return {"info" : "New follow created" }

    
    except Exception as ex:
        db.rollback()
        # Follow already exist
        if "Duplicate entry" in str(ex):
            response.status = 400
            return { "error_url" : "/home" }
        
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error" }
        
    
    finally:
        cursor.close()
        db.close()

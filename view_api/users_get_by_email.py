from bottle import get, request, response
import g
import pymysql

##############################

@get("/users/by-email/<user_email>")
def _(user_email):

    if not g.IS_VALID_EMAIL(user_email):
        response.status = 204
        return

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT user_id FROM users
            WHERE user_email = %s
            LIMIT 1""", (user_email,))
        user = cursor.fetchone()

        if not user:
            response.status = 204
            return
        
        response.status = 200
        return {"info" : "Email registered" }



    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error" }


    finally:
        db.close()
        cursor.close()

    



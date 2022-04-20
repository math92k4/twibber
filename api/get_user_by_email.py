from bottle import get, request, response
import g
import pymysql

##############################

@get("/get-user-by-email/<user_email>")
def _(user_email):
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT user_id FROM users
            WHERE user_email = %s""", (user_email,))
        user = cursor.fetchone()

        if not user:
            response.status = 204
            return
        
        response.status = 200
        return "Email registered"


    except Exception as ex:
        print(ex)
        response.status = 500
        return "Server error"

    finally:
        db.close()
        cursor.close()

    



from bottle import get, view, request, response, redirect
import g
import pymysql

##############################

@get("/update/<tweeb_id>")
@view("modals/update_tweeb")
def _(tweeb_id):
    is_xhr = True if request.headers.get("spa") else False
    if not is_xhr: 
        return redirect("/home")

    if not g.IS_VALID_SESSION(True):
        response.status = 400
        return { "error_url" : "/sign-out" }
    
    session = g.GET_DECODED_JWT()
    user_id = session["user_id"]

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE tweeb_id = %s
                        AND fk_user_id = user_id
                        AND user_id = %s""", (tweeb_id, user_id))
        tweeb = cursor.fetchone()

        if not tweeb:
            response.status = 204
            return
            
        return dict(tweeb = tweeb)
    
    except Exception as ex:
        print(ex)
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()
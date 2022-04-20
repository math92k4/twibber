from bottle import get, view, request, response
import g
import pymysql

##############################

# All tweets but the users
@get("/explore")
@view("main")
def _():
    is_xhr = True if request.headers.get("spa") else False
    session = g.GET_DECODED_JWT()

    if not session:
        user_id = 0
    else: 
        user_id = session["user_id"]
    
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE fk_user_id = user_id AND fk_user_id != %s
                        ORDER BY tweeb_created_at DESC""", (user_id,))
        tweebs = cursor.fetchall()
        return dict(
            is_xhr = is_xhr, 
            tweebs = tweebs,
            modules = {},
            session = session, 
            spa_url = "/explore",
            page_title = "Explore / Twibber",
            feed_title = "Explore",
            modal = None
            )

    except Exception as ex:
        print(ex)
        response.status = 500
        return "Server error"
    finally:
        cursor.close()
        db.close()
from bottle import get, view, response
import pymysql
import g

##############################

@get("/admin")
@view("admin/admin")
def _():
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE user_id = fk_user_id
                        ORDER BY tweeb_created_at DESC
                        LIMIT 10""", )
        tweebs = cursor.fetchall()

        # Determine to add "show more button"
        show_more_btn = True
        count = len(tweebs) 
        if count < 25:
            show_more_btn = False

        response.status = 200
        return dict(tweebs = tweebs, show_more_btn = show_more_btn) 

    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"
    
    finally:
        cursor.close()
        db.close()

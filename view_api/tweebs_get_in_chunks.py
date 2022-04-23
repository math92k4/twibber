from bottle import get, response, view
import pymysql
import g

##############################

@get("/tweebs/in-chunks/<chunk>")
def _(chunk):
    # VALIDATE chunk parameter
    try:
        chunk = int(chunk)
    except:
        response.status = 400
        return {"info" : "Chunk is not an int"}

    # CONNECT TO DB
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE user_id = fk_user_id
                        ORDER BY tweeb_created_at DESC
                        LIMIT %s, 10""", (chunk,))
        tweebs = cursor.fetchall()

        if not tweebs:
            response.status = 204
            return

        count = len(tweebs)

        response.status = 200
        return {"html" : tweebs_as_module(tweebs), "count" : str(count) }

    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server_error"}

    finally:
        cursor.close()
        db.close()


@view("admin/admin_tweebs")
def tweebs_as_module(tweebs):
    return dict(tweebs = tweebs)

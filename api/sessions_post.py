from bottle import post, request, response
import pymysql
import jwt
import re
import g


##############################
@post("/sessions")
def _():

    ##############################
    # VALIDATE

    user_email = request.forms.get("user_email")

    if len(user_email) > 50:
        return "woop"

    return str(len(user_email))

    if not g.IS_VALID_EMAIL(user_email):
        response.status = 400
        return {"error" : "user_email"}
    
    user_password = request.forms.get("user_password")
    return str(g.IS_VALID_PASSWORD(user_password))

    # user_password
    if (not request.forms.get("user_password")
        or not re.match(g.REGEX_PASSWORD, request.forms.get("user_password"))):
        response.status = 400
        return {"error" : "user_password"}
    user_password = request.forms.get("user_password")



    # VALIDATION COMPLETE
    ##############################
    # MATCH INFO WIDTH USER IN DB

    try:
        # CONNECT TO DB
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Find matching user & get column names and values
        # TODO - join session-id and use the same if exist
        cursor.execute("""SELECT * FROM users
                        WHERE user_email = %s 
                        AND user_password = %s""", (user_email, user_password))
        user = cursor.fetchone()

        # No match
        if not user:
            response.status = 400
            return {"error" : "Wrong email or password"}

        # SUCCES - create jwt
        encoded_jwt = jwt.encode(user, g.JWT_SECRET, algorithm="HS256")
        response.set_cookie("jwt", encoded_jwt)
        response.status = 200
        return {"info" : "jwt created"}

    ##############################

    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info" : "Server error" }

    ##############################
    
    finally:
        cursor.close()
        db.close()


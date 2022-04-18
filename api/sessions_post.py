from bottle import post, request, response
import pymysql
import jwt
import g

##############################
@post("/sessions")
def _():

    ##############################
    # VALIDATE

    user_email = request.forms.get("user_email")
    if not g.IS_VALID_EMAIL(user_email):
        response.status = 400
        return {"error_key" : "user_email"}
    
    user_password = request.forms.get("user_password")
    if not g.IS_VALID_PASSWORD(user_password):
        response.status = 400
        return {"error_key" : "user_password"}


    # VALIDATION COMPLETE
    ##############################
    # MATCH INFO WIDTH USER IN DB

    try:
        # CONNECT TO DB
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Does the email exist?
        cursor.execute("""SELECT user_email FROM users
                    WHERE user_email = %s""", (user_email))
        if not cursor.fetchone():
            response.status = 400
            return {"error_key" : "user_email", "error_message" : "Email not registered"}

        # Match password
        cursor.execute("""SELECT user_id, user_first_name, user_last_name, user_tag, user_created_at
                        FROM users
                        WHERE user_email = %s 
                        AND user_password = %s""", (user_email, user_password))
        user = cursor.fetchone()
        if not user:
            response.status = 400
            return {"error_key" : "user_password", "error_message" : "Incorrect password"}

        # Use already existing session_id if exists
        cursor.execute("""SELECT session_id FROM sessions
                        WHERE fk_user_id = %s""", (user["user_id"],))
        session = cursor.fetchone()

        if session:
            session_id = session["session_id"]

        else:
        # Insert new session to db
            cursor.execute("""INSERT INTO sessions (fk_user_id)
                            VALUES(%s)""", (user["user_id"],))
            session_id = cursor.lastrowid
            db.commit()

        # Insert session_id to user dict
        user["session_id"] = session_id

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


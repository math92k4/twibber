from bottle import post, request, response
import g
import time
import jwt
import pymysql

##############################

@post("/users")
def _():
    ##############################
    # VALIDATE

    # first name
    user_first_name = request.forms.get("user_first_name")
    if not g.IS_VALID_NAME(user_first_name):
        response.status = 400
        return {"error_key" : "user_first_name"}
    
    # last name
    user_last_name = request.forms.get("user_last_name")
    if not g.IS_VALID_NAME(user_last_name):
        response.status = 400
        return {"error_key" : "user_last_name"}
    
    # email
    user_email = request.forms.get("user_email")
    if not g.IS_VALID_EMAIL(user_email):
        response.status = 400
        return { "error_key" : "user_email" }

    # password
    user_password = request.forms.get("user_password")
    if not g.IS_VALID_PASSWORD(user_password):
        response.status = 400
        return {"error_key" : "user_password"}



    # VALIDATION COMPLETE
    ##############################
    # CREATE REMAING VALUES IN A TUPLE AND CONNECT TO DB

    user_tag = f"{user_first_name}{user_last_name}"
    user_created_at = int(time.time())
    
    # User tuple
    user = ( 
        user_first_name, 
        user_last_name, 
        user_email, 
        user_password, 
        user_tag, 
        user_created_at
    )

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # INSERT user
        cursor.execute("""INSERT INTO users (user_first_name, user_last_name, 
                user_email, user_password, user_tag, user_created_at)
                VALUES(%s, %s, %s, %s, %s, %s)""", user)
        user_id = cursor.lastrowid

        # INSERT session
        cursor.execute("""INSERT INTO sessions (fk_user_id)
                        VALUES(%s)""", (user_id,))
        session_id = cursor.lastrowid
        db.commit()

        # Create jwt to client
        jwt_user = {
            "session_id" : session_id,
            "user_id" : user_id,
            "user_first_name" : user_first_name,
            "user_last_name" : user_last_name,
            "user_email" : user_email,
            "user_tag" : user_tag,
            "user_created_at" : user_created_at
            }

        # SUCCES
        encoded_jwt = jwt.encode(jwt_user, g.JWT_SECRET, algorithm="HS256")
        response.set_cookie("jwt", encoded_jwt)
        response.status = 200
        return {"info" : f"User width id:{user_id} created"}


    ##############################

    except Exception as ex:
        print("#" * 30)
        print(ex)

        db.rollback() # Transaction rollback

        # If email exist in db
        if "user_email" in str(ex):
            response.status = 400
            return { "error_key" : "user_email", "error_message" : "Email already registered" }


        response.status = 500
        return {"info" : "Server error"}

    ##############################

    finally:
        cursor.close()
        db.close()



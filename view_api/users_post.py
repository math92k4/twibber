from bottle import post, request, response
import g
import time
import jwt
import pymysql
import uuid
import secrets
import datetime
import calendar

##############################

@post("/users")
def _():
    ##############################
    # VALIDATE DATA FROM CLIENT
    try:
        # first name
        user_first_name = request.forms.get("user_first_name")
        if not g.IS_VALID_NAME(user_first_name):
            response.status = 400
            return {"error_key" : "user_first_name"}
        user_first_name = user_first_name.capitalize()
        
        # last name
        user_last_name = request.forms.get("user_last_name")
        if not g.IS_VALID_NAME(user_last_name):
            response.status = 400
            return {"error_key" : "user_last_name"}
        user_last_name = user_last_name.capitalize()
        
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
        # CREATE REMAING VALUES IN A TUPLE 

        full_name = f"{user_first_name}{user_last_name}"
        user_tag = full_name[:20]
        user_created_at = int(time.time())
        date = datetime.datetime.fromtimestamp(user_created_at)
        user_created_at_date = f"{calendar.month_name[date.month]} {date.year}"

    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return {"info" : "Server error"}

    # CONNECT TO DB
    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # See if user_tag exists
        cursor.execute("""SELECT * FROM users
                        WHERE user_tag = %s
                        LIMIT 1""", (user_tag,))
        tag_exist = cursor.fetchone()

        # Generate and add key to tag, if exists - to make unique
        if tag_exist:
            unique_key = secrets.token_urlsafe(6)
            user_tag = f"{user_tag[:14]}{unique_key}"

        # Create user tuple
        user = ( 
            user_first_name, 
            user_last_name, 
            user_email, 
            user_password, 
            user_tag, 
            user_created_at,
            user_created_at_date
            )

        # INSERT user
        cursor.execute("""INSERT INTO users (user_first_name, user_last_name, 
                user_email, user_password, user_tag, user_created_at, user_created_at_date)
                VALUES(%s, %s, %s, %s, %s, %s, %s)""", user)
        user_id = cursor.lastrowid

        # INSERT session
        cursor.execute("""INSERT INTO sessions (fk_user_id)
                        VALUES(%s)""", (user_id,))
        session_id = cursor.lastrowid

        # INSERT verification
        verification_id = uuid.uuid4()
        cursor.execute("""INSERT INTO verifications (verification_id, fk_user_id)
                        VALUES(%s, %s)""", (verification_id, user_id))
        db.commit()

        # SUCCES
        # Create jwt to client
        jwt_user = {
            "session_id" : session_id,
            "user_id" : user_id,
            "user_first_name" : user_first_name,
            "user_last_name" : user_last_name,
            "user_email" : user_email,
            "user_tag" : user_tag,
            "user_created_at" : user_created_at,
            "user_icon_image" : None
            }

        try:
            g.SEND_VERIFICATION_EMAIL(user_email, verification_id)
        except Exception as ex:
            print("#"*30)
            print(str(ex))

        encoded_jwt = jwt.encode(jwt_user, g.JWT_SECRET, algorithm="HS256")

        response.set_cookie("jwt", encoded_jwt)
        response.status = 200
        return {"info" : f"User width id:{user_id} created"}


    ##############################

    except Exception as ex:
        print("#" * 30)
        print(str(ex))

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



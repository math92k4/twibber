from bottle import redirect, request, response
import pymysql
import jwt
import re

##############################

# REGEX
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$"
REGEX_NAME = '^[A-Za-z]{2,}$'

# SECRETS
JWT_SECRET = "THISkeyISIpossibleToGet123321123"

# DB CONFIGURATION
DB_CONFIG = {
    "host" : "localhost",
    "user" : "root",
    "port" : 8889,
    "password" : "root",
    "database" : "twibber",
    "cursorclass":pymysql.cursors.DictCursor
}

##############################

def GET_DECODED_JWT():
    if not request.get_cookie("jwt"):
        return False
    encoded_jwt = request.get_cookie("jwt")
    decoded_jwt = jwt.decode(encoded_jwt, JWT_SECRET, algorithms=["HS256"])
    return decoded_jwt

##############################
# VALIDATION

def IS_VALID_SESSION(is_xhr = False):
    # No jwt
    if not request.get_cookie("jwt"):
        return False
    
    # Get jwt
    decoded_jwt = GET_DECODED_JWT()

    if decoded_jwt == False:
        if is_xhr:
            return False
        return redirect("/sign-out")

    # Connect to db
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()
        session = (decoded_jwt["session_id"], decoded_jwt["user_id"])
        cursor.execute("""SELECT * FROM sessions
                        WHERE session_id = %s AND fk_user_id = %s""", session)

        if not cursor.fetchone():
            if is_xhr: return False
            return redirect("/sign-out")
        
        # Succes
        return True
    
    except Exception as ex:
        print(ex)
        response.status = 500
        if is_xhr:
            return False
        return redirect("/sign-out")


    finally:
        cursor.close()
        db.close()

##############################

def IS_VALID_EMAIL(string):
    if not string:
        return False
    if not re.match(REGEX_EMAIL, string):
        return False
    if len(string) > 50:
        return False
    return True

##############################

def IS_VALID_PASSWORD(string):
    if not string:
        return False
    if not re.match(REGEX_PASSWORD, string):
        return False
    if len(string) > 30 or len(string) < 8:
        return False
    return True

##############################

def IS_VALID_NAME(string):
    if not string:
        return False
    if not re.match(REGEX_NAME, string):
        return False
    if len(string) > 20 or len(string) < 2:
        return False
    return True
    

    


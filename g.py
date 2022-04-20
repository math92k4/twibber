from bottle import redirect, request, response
import pymysql
import jwt
import re
import time

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

##############################

# REGEX
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$"
REGEX_NAME = '^[A-Za-z]{2,}$'
REGEX_UUID4 = '^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'

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

def SEND_VERIFICATION_EMAIL(user, verification_id):
    sender_email = "matkeatest@gmail.com"
    receiver_email = user["user_email"]
    password = "ASDasd123!"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to Twibber"
    message["From"] = sender_email
    message["To"] = receiver_email

    verification_link = f"127.0.0.1:5555/verify-email/{verification_id}"

    # Create the plain-text and HTML version of your message
    text = f"""\
    Welcome to Twibber
    
    Visit the URL below to verify your email.
    {verification_link}
    """

    html = f"""\
    <html>
        <body>
        <p>
            <b>Welcome to Twibber</b><br>
            Visit this link to verify your email:
            {verification_link}
        </p>
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return "yes, email sent"
        except Exception as ex:
            print(ex)
            return "uppps... could not send the email"
    

##############################

def CALC_TIME_AGO(tweeb_epoch):
    print("#"*30)
    print(tweeb_epoch)
    currunt_epoch = int(time.time())
    epoch_since = currunt_epoch - tweeb_epoch

    if epoch_since > 31556926:
        time_since_tweeb = int(epoch_since / 31556926)
        return f"{time_since_tweeb}y"    
    elif epoch_since > 86400:
        time_since_tweeb = int(epoch_since / 86400)
        return f"{time_since_tweeb}d"
    elif epoch_since > 3600 :
        time_since_tweeb = int(epoch_since / 3600)
        return f"{time_since_tweeb}h"
    elif epoch_since > 60:
        time_since_tweeb = int(epoch_since / 60)
        return f"{time_since_tweeb}m"
    elif epoch_since > 10:
        time_since_tweeb = epoch_since
        return f"{time_since_tweeb}s"
    
    return f"Now"

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
    

    


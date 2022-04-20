from bottle import post, request, response, view
import g
import re
import pymysql
import time
import os
import uuid
import imghdr

##############################

@post("/tweebs")
def _():
    #VALIDATE
    # Session
    if not g.IS_VALID_SESSION(True):
        response.status = 400
        return {"error_url" : "/sign-out"}
    session = g.GET_DECODED_JWT()

    # Tweeb_text
    tweeb_text = request.forms.get("tweeb_text")
    if not tweeb_text:
        response.status = 400
        return {"error_key" : "tweeb_text", "error_message" : "Please enter a tweeb text"}

    tweeb_text = re.sub("[\n]*", "", tweeb_text)
    tweeb_text = re.sub(" +", " ", tweeb_text)
    tweeb_text = tweeb_text.strip()
    if len(tweeb_text) > 100 or len(tweeb_text) < 1:
        response.status = 400
        return {"error_key" : "tweeb_text", "error_message" : "A tweeb text must be at least 1 and max 100 characters"}


    # Tweeb image (optional)
    tweeb_image = None
    if request.files.get("tweeb_image"):
        image = request.files.get("tweeb_image")
    
        # Get file extension
        file_name, file_extension = os.path.splitext(image.filename)

        # Validate extension
        if file_extension not in (".png", ".jpeg", "jpg"):
            response.status = 400
            return f"Filetype: {file_extension} not allowed"

        # Make .jpg = .jpeg for imghdr validation
        if file_extension == ".jpg":
            file_extension = ".jpeg"

        # Create new db-friendly file-name
        image_id = str(uuid.uuid4())
        tweeb_image = f"{image_id}{file_extension}"

        # Save image in images dir
        image.save(f"assets/images/{tweeb_image}")

        # Validate that the file is not manipulated (post upload)
        imghdr_extension = imghdr.what(f"assets/images/{tweeb_image}")
        if not file_extension == f".{imghdr_extension}":
            os.remove(f"assets/images/{tweeb_image}")
            response.status = 400
            return "File manipulated. This is not an image.."


    # Set remaining values
    fk_user_id = session["user_id"]
    tweeb_created_at = int(time.time())
    tweeb_updated_at = int(time.time())


    tweeb_tuple = (
        fk_user_id,
        tweeb_text,
        tweeb_image,
        tweeb_created_at,
        tweeb_updated_at
    )

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # INSERT tweeb
        cursor.execute("""INSERT INTO tweebs (fk_user_id, tweeb_text, tweeb_image, tweeb_created_at, tweeb_updated_at)
                VALUES(%s, %s, %s, %s, %s)""", tweeb_tuple)
        tweeb_id = cursor.lastrowid
        db.commit()

        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE tweeb_id = %s
                        AND fk_user_id = user_id""", (tweeb_id,))
        tweeb = cursor.fetchone()


        print("#"*30)
        print(tweeb)
        return get_tweeb_as_module(tweeb, session)

    except Exception as ex:
        print(ex)
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()

@view("parts/tweeb")
def get_tweeb_as_module(tweeb, session):
    return dict(tweeb = tweeb, session = session)

##############################
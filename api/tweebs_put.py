from bottle import put, request, response, view
import pymysql
import g
import os
import time
import re
import uuid
import imghdr
import json

##############################

@put("/tweebs")
@view("parts/tweeb")
def _():
    # VALIDATE 
    # session
    if not g.IS_VALID_SESSION(True):
        response.status = 400
        return {"error_url" : "/sign-out"}
    session = g.GET_DECODED_JWT()

    # Get tweeb-id
    tweeb_id = request.forms.get("tweeb_id")
    if not tweeb_id: 
        response.status = 204
        return

    try:
        # Get old tweeb from db - and validate existens and ownership
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM tweebs
                        WHERE tweeb_id = %s
                        AND fk_user_id = %s""", (tweeb_id, session["user_id"]))
        tweeb = cursor.fetchone()

        if not tweeb:
            response.status = 204
            return
        
        # tweeb_text
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


        # Get old image and determine tweeb_image
        old_image = request.forms.get("old_tweeb_image")

        # If updated tweeb = tweeb in db - stop excecuting
        if old_image and tweeb_text == tweeb["tweeb_text"]:
            response.status = 204
            return

        if not old_image:

            tweeb_image = None
            image = request.files.get("tweeb_image")
            if image:
                # VALIDATE IMAGE
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

        else: tweeb_image = old_image

        tweeb_updated_at = int(time.time())
        tweeb_tuple = (
            tweeb_text,
            tweeb_image,
            tweeb_updated_at,
            tweeb_id,
            session["user_id"]            
        )
        
        # UPDATE TWEEB
        cursor.execute("""UPDATE tweebs
                        SET tweeb_text = %s, tweeb_image = %s, tweeb_updated_at = %s
                        WHERE tweeb_id = %s AND fk_user_id = %s""", tweeb_tuple)
        db.commit()

        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE tweeb_id = %s""", (tweeb_id,))
        updated_tweeb = cursor.fetchone()
        
        # SUCCES
        # If image was updated - delete the old image from server
        if not old_image and tweeb["tweeb_image"]:
            os.remove(f"assets/images/{tweeb['tweeb_image']}")

        return dict(session = session, tweeb = updated_tweeb)


    except Exception as ex:
        print(ex)
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()


from bottle import get, response, redirect
import g
import re
import pymysql

##############################

@get("/verify-email/<verification_id>")
def _(verification_id):
    # VALIDATE
    # uuid
    if not re.match(g.REGEX_UUID4, verification_id):
        response.status = 400
        return "No account to verify..."

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        
        # GET verication row
        cursor.execute("""SELECT * FROM verifications
                        WHERE verification_id = %s""", (verification_id,))
        verification = cursor.fetchone()
        if not verification:
            response.status = 400
            return "No account to verify..."

        # DELETE verification row
        cursor.execute("""DELETE FROM verifications
                        WHERE verification_id = %s""", (verification_id,))

        # UPDATE user verification-status
        cursor.execute("""UPDATE users
                        SET user_verified = 1
                        WHERE user_id = %s""", (verification["fk_user_id"],))
        db.commit()

    except Exception as ex:
        db.rollback()
        print(ex)
        response.status = 500
        return "Server error"
    
    finally:
        cursor.close()
        db.close()


    return redirect("/home")

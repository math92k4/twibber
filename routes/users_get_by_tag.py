from bottle import get, view, request, response
import pymysql
import g

# All tweets from specific user
@get("/<user_tag>")
@view("main")
def _(user_tag):
    is_xhr = True if request.headers.get("spa") else False
    session = g.GET_DECODED_JWT()

    # VALIDATE user_tag - because of secret-key, it can contain any symbol
    if len(user_tag) > 20:
        # status 200 because 204 will return nothing
        response.status = 200
        return user_204(is_xhr, session, user_tag)

    try:
        db = pymysql.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Is user in db?
        cursor.execute("""SELECT * FROM users
                        WHERE user_tag = %s
                        LIMIT 1""", (user_tag,))
        user = cursor.fetchone()

        if not user:
            response.status = 200
            return user_204(is_xhr, session, user_tag)

        # Get user tweebs
        cursor.execute("""SELECT * FROM tweebs
                        JOIN users
                        WHERE fk_user_id = user_id 
                        AND user_tag = %s
                        ORDER BY tweeb_created_at DESC
                        LIMIT 25""", (user_tag,))
        tweebs = cursor.fetchall()

        # If has session and other user exist - see if follows
        is_following = False
        if session and user:
            follower_id = session["user_id"]
            following_id = user["user_id"]
            cursor.execute("""SELECT * FROM follows
                            WHERE follower_id = %s 
                            AND following_id = %s
                            LIMIT 1""", (follower_id, following_id))
            if cursor.fetchone():
                is_following = True


        feed_title = f"{user['user_first_name']} {user['user_last_name']}"
        page_title = f"{user['user_first_name']} {user['user_last_name']} (@{user['user_tag']}) / Twibber"

        response.status = 200
        return dict(
            is_xhr = is_xhr,
            tweebs = tweebs,
            modules = {"profile_section"},
            user = user,
            is_following = is_following,
            session = session, 
            spa_url = f"/{user_tag}",
            page_title = page_title,
            feed_title = feed_title,
            modal = None
            )


    except Exception as ex:
        print("#"*30)
        print(str(ex))
        response.status = 500
        return "Server error"
    finally:
        cursor.close()
        db.close()


def user_204(is_xhr, session, user_tag):
            feed_title = "Profile"
            page_title = "Profile / Twibber"
            return dict(
                is_xhr = is_xhr,
                tweebs = {},
                modules = {"profile_section"},
                user = False,
                is_following = False,
                session = session, 
                spa_url = f"/{user_tag}",
                page_title = page_title,
                feed_title = feed_title,
                modal = None
                )
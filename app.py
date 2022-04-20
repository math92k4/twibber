from bottle import run

##############################

# Routes
import routes.static_routes

import routes.index_get
import routes.sign_out_get
import routes.sign_up_get
import routes.sign_in_get

import routes.home_get
import routes.explore_get
import routes.users_get_by_tag
import routes.compose_tweeb_get
import routes.update_tweebs_by_id

import routes.verify_email_get

# API's
import api.tweebs_post
import api.users_post
import api.sessions_post
import api.get_user_by_email
import api.tweebs_delete_by_id
import api.follows_post
import api.follows_delete
import api.tweebs_put

##############################
##############################
##############################

try:
    # Prod
    import production
    application = default_app()
except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )
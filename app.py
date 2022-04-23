from bottle import run, default_app

##############################

# Routes
import routes.static_routes

# Admin
import routes.admin_get
import view_api.tweebs_get_in_chunks
import view_api.tweebs_delete_by_id_as_admin

# Main Routes
import routes.index_get
import routes.sign_out_get
import routes.sign_up_get
import routes.sign_in_get

import routes.home_get
import routes.explore_get
import routes.users_get_by_tag
import routes.compose_tweeb_get
import routes.update_tweebs_get_by_id

import routes.verify_email_get

# VIEW_APIs
# RETURNS html and / or status codes on succes
# RETURNS json on errors - handled by "handleServerValidation" (js)
import view_api.tweebs_post
import view_api.users_post
import view_api.sessions_post
import view_api.users_get_by_email
import view_api.tweebs_delete_by_id
import view_api.follows_post
import view_api.follows_delete
import view_api.tweebs_put

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
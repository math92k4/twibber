# VALIDATION
- Instant front-end validation via html and css
- Tweeb-text-validation / autocorrecting white-space " " + "\n"
- Instant email validation via API when signing up
- Backend validation errors, with possibility for costumized errors, is displayed and handled via the API response (handleServeValidation)


# SEO-friendly single-page-app
- Bridge between the front-page, main-page
- Otherwise all URLs will be rendered dynimacally with url-update, page-title-update, and history-back-forth compability
- Every url (except /update/tweeb_id) can also be rendered server-side


# URL-list
- /                    Front-page                           no-session only
- /sign-up             Front-page + modal                   no-session only
- /sign-in             Front-page + modal                   o-session only

- /sign-out            only redirect                        No content

- /home                Your tweebs + those you follow       session only
- /compose/tweeb       /home + modal                        session only
- /update/<tweeb_id>   /home + modal                        session only - if not ajax: redirect /home

- /explore             All tweebs but your own              Open access
- /<user_tag>          Tweebs by the user                   Open access

# /admin               All tweebs                           Open acces


# Features
- Sign up
- Sign in
- Verify account via email link
- Create tweet
- Like Tweeb
- Upload image to tweeb
- Update your own tweets
- Delete your own tweets
- Follow user
- Unfollow user







# REQUIREMENTS

- Sign Up - DONE

- Sign In / login - DONE

- Logout - Simple page or SPA if you want to - DONE

- Use a session - DONE

- Use a JWT - DONE

- Tweet - DONE

- Delete tweet -  DONE

- Update tweet -  DONE

- Follow someone -  DONE

- See pages from other users - DONE

# Choose 1 extra functionality

- Verification email when signing up - DONE

- Upload image in system - DONE

# Admin panel

Admin panel must - This is a "stand-alone" feature. This means that it doesn't have to be part of the twitter application, but can be a whole different solution. The administrator can see all tweets and delete them if wanted. It is a SPA, so deleting a tweet doesn't reload the whole page








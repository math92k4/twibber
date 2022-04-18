# VALIDATION
- Instant front-end validation via html and css
- Tweeb-text-validation / autocorrecting white-space " " + "\n"
- Instant email validation via API when signing up
- Backend validation errors, with possibility for costumized errors, is displayed and handled via the API response (handleServeValidation)


# SEO-friendly single-page-app
- Bridge between the front-page, main-page
- Otherwise all URLs will be rendered dynimacally with url-update, page-title-update, and history-back-forth compability
- Every url can also be rendered server-side


# URL-list
- /                                 no-session only
- /sign-up                          no-session only
- /sign-in                          no-session only

- /sign-out                         No content, only redirect

- /home                             session only

- /explore                          Open access
- /<user_tag>                       Open acces
- /<user_tag>/tweeb/<tweeb_id>      Open acces

- /admin                            Open acces - Rights to delete tweets and users


# Features
- Like Tweeb
- Follow user
- Create tweet
- Upload image to tweeb
- Update your own tweets
- Delete your own tweets






# A user must be able to:



- Sign Up - DONE

- Sign In / login - DONE

# Logout - Simple page or SPA if you want to - DONE

- Use a session - DONE

- Use a JWT - DONE

- Tweet - DONE

- Delete tweet -  DONE

# Update tweet -  It is a SPA, the page should not reload

- Follow someone -  DONE

- See pages from other users - DONE

# Choose 1 extra functionality

# Optional - Send an email when the user creates an account (Sign up). 

- Upload image in system - DONE

# Admin panel

Admin panel must - This is a "stand-alone" feature. This means that it doesn't have to be part of the twitter application, but can be a whole different solution. The administrator can see all tweets and delete them if wanted. It is a SPA, so deleting a tweet doesn't reload the whole page








#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""oauth2-facebook.py: Implementing OAuth2 Login for Facebook."""

# Guidelines:
# 1. Register your account as a developer at https://developers.facebook.com/.
# 2. Create New App at: https://developers.facebook.com/apps/.
# 3. On https://developers.facebook.com/apps/<app_id>/summary, do the following:
#    * Get App ID: (e.g. 545723862164937)
#      - This is your client_id
#    * Get App Secret: (e.g. 5407608c6e9d10b297ba77a4de18f75f)
#      - This is your client_secret
#    * On App Domains: (e.g. mydomain.tld)
#    * On Sandbox Mode:
#      - Click Disabled to let non-developer accounts test the app
#    * Under the "Select how your app integrates with Facebook",
#      click the "Website with Facebook Login"
#    * Click Save Changes

import bottle as app
import rauth

import config

oauth2 = rauth.OAuth2Service
facebook = oauth2(
    client_id=config.FACEBOOK_CLIENT_ID,
    client_secret=config.FACEBOOK_CLIENT_SECRET,
    name='facebook',
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/'
)
redirect_uri = '{uri}:{port}/success'.format(
    uri=config.BASE_URI,
    port=config.PORT
)

@app.route('/')
def index():
    return '<a href="/login">Log in using Facebook</a>'

@app.route('/login<:re:/?>')
def login():
    params = dict(
        scope='read_stream',
        response_type='code',
        redirect_uri=redirect_uri
    )
    url = facebook.get_authorize_url(**params)

    app.redirect(url)

@app.route('/success<:re:/?>')
def login_success():
    code = app.request.params.get('code')
    session = facebook.get_auth_session(
        data=dict(
            code=code,
            redirect_uri=redirect_uri
        )
    )
    session_json = session.get('me').json()
    # For complete list of keys,
    # go to: https://developers.facebook.com/docs/reference/api/user/
    return 'Welcome {name}!'.format(**session_json)

app.run(
    server=config.SERVER,
    port=config.PORT,
    host=config.HOST
)

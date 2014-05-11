#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""oauth1-twitter.py: Implementing OAuth1 Login for Twitter."""

# Guidelines:
# Note: Twitter uses OAuth1, not OAuth2
# 1. Create New App at: https://dev.twitter.com/apps/new
# 2. On the Application Details, specify the following:
#    * Name: (e.g. My XYZ App)
#    * Description: (e.g. Test App for My App)
#    * Website: (e.g. mydomain.tld)
#    * Callback URL: (e.g. http://mydomain.tld/success)
#    * Click the "Yes, I agree" checkboxk
#    * On the CAPTCHA, enter the image texts
#    * Click the Create your Twitter application
# 3. On the https://dev.twitter.com/apps/<app_id>/show, do the following:
#    * Get the Consumer key: (e.g. 07gvoVMGyyul4m5bKkJuOA)
#      - This is your consumer_key
#    * Get the Consumer secret:
#      - (e.g. PUOGZog1IhxsOQVojrwVgjHgSlHaVRibcpVsP8Axk0)
#      - This is your consumer_secret
#    * Under "Your access token", click Create my access token

import bottle as app
import rauth

import config

oauth1 = rauth.OAuth1Service
twitter = oauth1(
    consumer_key=config.TWITTER_CLIENT_ID,
    consumer_secret=config.TWITTER_CLIENT_SECRET,
    name='twitter',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/'
)
request_token, request_token_secret = twitter.get_request_token()
authorize_url = twitter.get_authorize_url(request_token)

@app.route('/')
def index():
    return '<a href="/login">Log in using Twitter</a>'

@app.route('/login<:re:/?>')
def login():
    app.redirect(authorize_url)

@app.route('/success<:re:/?>')
def login_success():
    oauth_token = app.request.params.get('oauth_token')
    oauth_verifier = app.request.params.get('oauth_verifier')
    session = twitter.get_auth_session(
        request_token,
        request_token_secret,
        method='POST',
        data=dict(oauth_verifier=oauth_verifier)
    )
    params = {}
    # For complete list of parameters for verify_credentials,
    # go to: https://dev.twitter.com/docs/api/1.1/get/account/verify_credentials
    # Note: This same technique applies to other json_path, just got to its page
    #       and the parameters can be found there

    json_path = 'account/verify_credentials.json'
    session_json = session.get(json_path, params=params, verify=True).json()
    # For non-Ascii characters to work properly!
    session_json = dict((k, unicode(v).encode('utf-8')) for k, v in session_json.iteritems())
    # For complete list of json_path,
    # go to: https://dev.twitter.com/docs/api/1.1
    return 'Welcome {name}!'.format(**session_json)

app.run(
    server=config.SERVER,
    port=config.PORT,
    host=config.HOST
)

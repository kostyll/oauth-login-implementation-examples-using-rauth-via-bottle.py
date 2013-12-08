#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""oauth2-google.py: Implementing OAuth2 Login for Google."""

# Guidelines for rauth via Google API:
# 1. Create project at:
#    https://cloud.google.com/console?redirected=true#/project?redirected=true
# 2. On the New Project, specify the following:
#    * Project name: (e.g. My XYZ App)
#    * Project ID: (e.g. my-xyz-app)
# 3. Go to: https://code.google.com/apis/console/#:access
#    * Click Edit branding information... and specify the following:
#      * Product name: (e.g. My XYZ App)
#      * Click Update
#    * Click Create another client ID... and specify the following:
#      * On Application type, select Web application (default)
#      * Under Your site or hostname:
#        * Click more options:
#          * Under the Authorized Redirect URIs, type the following:
#            - http://localhost:8000/success
#          * Under the Authorized JavaScript Origins, type the following:
#            - http://localhost:8000
#          * Click Create client ID
#   * Under the Client ID for web applications, get the following:
#     * Client ID: (e.g. 954851881468.apps.googleusercontent.com)
#     * Client secret: (e.g. HTvpTPPUGQfWByCaonsC4EMa)

import json

import bottle as app
import rauth

import config

oauth2 = rauth.OAuth2Service
google = oauth2(
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    name='google',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    base_url='https://accounts.google.com/o/oauth2/auth',
)
redirect_uri = '{uri}:{port}/success'.format(
    uri=config.GOOGLE_BASE_URI,
    port=config.PORT
)

@app.route('/')
def index():
    return '<a href="/login">Log in using Google</a>'

@app.route('/login<:re:/?>')
def login():
    params = dict(
        scope='email profile',
        response_type='code',
        redirect_uri=redirect_uri
    )
    url = google.get_authorize_url(**params)

    app.redirect(url)

@app.route('/success<:re:/?>')
def login_success():
    code = app.request.params.get('code')
    session = google.get_auth_session(
        data=dict(
            code=code,
            redirect_uri=redirect_uri,
            grant_type='authorization_code'
        ),
        decoder=json.loads
    )
    json_path = 'https://www.googleapis.com/oauth2/v1/userinfo'
    session_json = session.get(json_path).json()
    return 'Welcome {name}!'.format(**session_json)
    # Unfortunately, there seem to be no reference for complete list of keys,
    # but here are the complete json keys returned by the scope: email profile:
    # * email
    # * family_name
    # * gender
    # * given_name
    # * id
    # * link
    # * locale
    # * name
    # * picture

app.run(
    server=config.SERVER,
    port=config.PORT,
    host=config.HOST
)

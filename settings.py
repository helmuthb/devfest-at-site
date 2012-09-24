import os
from google.appengine.api.app_identity import get_default_version_hostname, get_application_id

from secrets import SESSION_KEY

# trigger pybabel extraction of strings
dev _(arg):
  return arg

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG = True
    HOME_URL = 'http://localhost' + ':8085'
else:
    DEBUG = False
    HOME_URL = 'http://' + get_default_version_hostname()

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
}

# i18n config
AVAILABLE_LOCALES = ['en_US', 'de_DE']

# List of valid APIs
APIS = frozenset({'signup_mailing_list', 'change_email_addr'})

#200 OK - Everything worked as expected.
#400 Bad Request - Often missing a required parameter.
#401 Unauthorized - No valid API key provided.
#402 Request Failed - Parameters were valid but request failed.
#404 Not Found - The requested item doesn't exist.
#500, 502, 503, 504 Server errors - something went wrong on Stripe's end.

API_CODES  = { 200 : _('Success'),
               400 : {'email'       : _('Invalid email address'),
                      'password'    : _('Invalid password'),
                      'email_password' : _('Invalid email or password'),
                      'unsupported' : _('Unsupported API'),
                      'missing'     : _('Not all parameter present'),
                      'noemail'     : _('Email not valid')},
               401 : _('Unauthorized'),
               402 : {'unconfirmed' : _('Email has not been confirmed.'),
                      'duplicate'   : _('User already exists.')},
               404 : _('Does not exist'),
               500 : {'generic'        : _('Server error'),
                      'admin_required' : _('Please contact application administrator for support')}}

# URLs
APP_ID = get_application_id()

COOKIE_TEMPLATE = { 'id'        : 0,     #session id
                    'pageviews' : 0, 
                    'authed'    : False, 
                    'active'    : True }

DATE_FORMAT_HTML = _("yyyy-mm-dd")
DATE_FORMAT = _("%Y-%m-%d")

# Email Authentication
EMAIL_CONFIRM_BODY = _("""
Hello, %s!

Please click the link below to confirm your email address: 

%s

Thank you.
""")

EMAIL_SENDER = "DevFest Team <team@devfest.at>"

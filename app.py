import webapp2

import settings
from handlers import index, form, api, common, email_auth, locale, json

routes = [webapp2.Route('/',                  handler = index.Index),
          webapp2.Route('/location',          handler = index.Location),
          webapp2.Route('/agenda',            handler = index.Agenda),
          webapp2.Route('/agenda2',           handler = index.Agenda2),
          webapp2.Route('/call',              handler = index.Call),
          webapp2.Route('/sponsor',           handler = index.Sponsor),
          webapp2.Route('/session/<url>',     handler = index.Session),
          webapp2.Route('/speakers',          handler = index.Speakers),
          webapp2.Route('/image/<id>',        handler = index.ObjectImage),
          webapp2.Route('/editsession/<id>',  handler = form.EditSession),
          webapp2.Route('/editsession',       handler = form.EditSession),
          webapp2.Route('/editspeaker/<id>',  handler = form.EditSpeaker),
          webapp2.Route('/editspeaker',       handler = form.EditSpeaker),

          # JSON results for Android app
          webapp2.Route('/json/sessions',     handler = json.JsonSessions),
          webapp2.Route('/json/speakers',     handler = json.JsonSpeakers),
          webapp2.Route('/json/news',         handler = json.JsonNews),
          webapp2.Route('/json/rooms',        handler = json.JsonRooms),
          webapp2.Route('/json/slots',        handler = json.JsonSlots),
          webapp2.Route('/json/tracks',       handler = json.JsonTracks),
          webapp2.Route('/json/suggests',     handler = json.JsonSuggests),
          webapp2.Route('/json/sponsors',     handler = json.JsonSponsors),
          
          # email authentication routes
          webapp2.Route('/email-confirm',     handler = email_auth.EmailConfirm),
          webapp2.Route('/email-signin',      handler = email_auth.EmailAuthHandler, handler_method="signin_email"),
          webapp2.Route('/email-signup',      handler = email_auth.EmailAuthHandler, handler_method="signup_email"),
          
          # oauth authentication routes
          webapp2.Route('/auth/<provider>',   handler='handlers.oauth.AuthHandler:simple_auth', name='auth_login'),
          webapp2.Route('/auth/<provider>/callback', handler='handlers.oauth.AuthHandler:_auth_callback', name='auth_callback'),
          
          # common logout
          webapp2.Route('/logout', handler='handlers.oauth.AuthHandler:logout', name='logout'),
          
          # i18n manual locale change
          webapp2.Route('/locale/<locale>', handler=locale.SetLocale),

          ]                             
                                       
application = webapp2.WSGIApplication(routes,   
                                      debug = settings.DEBUG,
                                      config = settings.app_config)

application.error_handlers[404] = common.handle_404
application.error_handlers[500] = common.handle_500

def main():
    application.run()

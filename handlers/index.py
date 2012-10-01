import common
import logging
from google.appengine.ext import ndb
from core import model
from webapp2_extras import i18n

class Index(common.BaseHandler):
  def get(self):
    self.prep_html_response('index.html')

class Location(common.BaseHandler):
  def get(self):
    self.prep_html_response('location.html')

class Agenda(common.BaseHandler):
  def get(self):
    self.prep_html_response('agenda.html')

class Sponsor(common.BaseHandler):
  def get(self):
    self.prep_html_response('sponsor.html')

class Call(common.BaseHandler):
  def get(self):
    self.prep_html_response('call.html')

class Session(common.BaseHandler):
  def get(self, url):
    session = model.SessionTalk.query(model.SessionTalk.url == url).fetch(1)[0]
    speakers = [ sp.get() for sp in session.speaker ]
    # work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    if locale[0:2] == "de":
      session.title = session.title_de
      session.abstract = session.abstract_de
      for sp in speakers:
        sp.bio = sp.bio_de
    else:
      session.title = session.title_en
      session.abstract = session.abstract_en
      for sp in speakers:
        sp.bio = sp.bio_en
    self.prep_html_response('session.html', {'session':session, 'speakers':speakers})

class ObjectImage(common.BaseHandler):
  def get(self, id):
    object = ndb.Key(urlsafe = id).get()
    mime = 'image/png'
    if object.image[1:4] == 'PNG':
      mime = 'image/png'
    elif object.image[0:3] == 'GIF':
      mime = 'image/gif'
    elif object.image[6:10] == 'JFIF':
      mime = 'image/jpeg'
    self.response.headers['Content-Type'] = mime
    self.response.out.write(object.image)


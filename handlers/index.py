import common
import logging
import random
from google.appengine.ext import ndb
from core import model
from webapp2_extras import i18n

class Index(common.BaseHandler):
  def get(self):
    # get the images...
    list = [ '/img/pics/image_' + str(i) + '.jpg' for i in range(70) ]
    random.shuffle(list)
    self.prep_html_response('index.html', {'images':list})

class Index2(common.BaseHandler):
  def get(self):
    # get the images...
    list = [ '/img/pics/image_' + str(i) + '.jpg' for i in range(70) ]
    random.shuffle(list)
    self.prep_html_response('index2.html', {'images':list})
    
class Location(common.BaseHandler):
  def get(self):
    self.prep_html_response('location.html')

class Agenda(common.BaseHandler):
  def get(self):
    self.prep_html_response('agenda.html')

class Sessions(common.BaseHandler):
  def get(self, event='2012'):
    sessions = model.SessionTalk.query(model.SessionTalk.event == event).fetch()
    # work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    if locale[0:2] == "de":
      for session in sessions:
        session.title = session.title_de
        session.abstract = session.abstract_de
    else:
      for session in sessions:
        session.title = session.title_en
        session.abstract = session.abstract_en
    self.prep_html_response('sessions.html', {'event':event,'sessions':sessions})

class Agenda2(common.BaseHandler):
  def get(self):
    self.prep_html_response('agenda2.html')

class Sponsor(common.BaseHandler):
  def get(self):
    self.prep_html_response('sponsor.html')

class Call(common.BaseHandler):
  def get(self):
    # work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    self.prep_html_response('call.html')

class Session(common.BaseHandler):
  def get(self, url, event='2012'):
    session = model.SessionTalk.query(ndb.AND(model.SessionTalk.event == event, model.SessionTalk.url == url)).fetch(1)[0]
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
      for link in session.link:
        link.text = link.text_de
    else:
      session.title = session.title_en
      session.abstract = session.abstract_en
      for sp in speakers:
        sp.bio = sp.bio_en
      for link in session.link:
        link.text = link.text_en
    self.prep_html_response('session.html', {'event':event, 'session':session, 'speakers':speakers})

class Speakers(common.BaseHandler):
  def get(self, event='2012'):
    speakers = model.Speaker.query(model.Speaker.event == event).order(model.Speaker.url).fetch()
    # work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    if locale[0:2] == "de":
      for sp in speakers:
        sp.bio = sp.bio_de
    else:
      for sp in speakers:
        sp.bio = sp.bio_en
    self.prep_html_response('speakers.html', {'event':event, 'speakers':speakers})

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


import common
import logging
import random
from google.appengine.ext import ndb
from google.appengine.api import images, memcache
from core import model
from webapp2_extras import i18n

# list of level texts
leveltext_de = { '101':'101 - f&uuml;r Anf&auml;ngerInnen geeignet', '201':'201 - m&auml;&szlig;ig Fortgeschrittene', '301':'301 - ExpertInnenniveau' }
leveltext_en = { '101':'101 - suited for beginners', '201':'201 - intermediate experience', '301':'301 - expert level' }

# list of language texts
languagetext_de = { 'en':'Englisch', 'de':'Deutsch', 'en-pref':'Englisch, auf Wunsch auch Deutsch', 'de-pref':'Deutsch, auf Wunsch auch Englisch' }
languagetext_en = { 'en':'English', 'de':'German', 'en-pref':'English, on request also German', 'de-pref':'German, on request also English' }

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
    for session in sessions:
      session.speakers = [ sp.get() for sp in session.speaker ]
    if locale[0:2] == "de":
      for session in sessions:
        session.title = session.title_de
        session.abstract = session.abstract_de
        session.requirements = session.requirements_de
        if session.language:
          session.languagetext = languagetext_de[session.language]
        if session.level:
          session.leveltext = leveltext_de[session.level]
    else:
      for session in sessions:
        session.title = session.title_en
        session.abstract = session.abstract_en
        session.requirements = session.requirements_en
        if session.language:
          session.languagetext = languagetext_en[session.language]
        if session.level:
          session.leveltext = leveltext_en[session.level]
    self.prep_html_response('sessions.html', {'event':event,'sessions':sessions})

class Agenda2(common.BaseHandler):
  def get(self):
    self.prep_html_response('agenda2.html')

class Sponsor(common.BaseHandler):
  def get(self):
    self.prep_html_response('sponsor.html')

class Policy(common.BaseHandler):
  def get(self):
    self.prep_html_response('policy.html')

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
      session.requirements = session.requirements_de
      for sp in speakers:
        sp.bio = sp.bio_de
      for link in session.link:
        link.text = link.text_de
      if session.language:
        session.languagetext = languagetext_de[session.language]
      if session.level:
        session.leveltext = leveltext_de[session.level]
    else:
      session.title = session.title_en
      session.abstract = session.abstract_en
      session.requirements = session.requirements_en
      for sp in speakers:
        sp.bio = sp.bio_en
      for link in session.link:
        link.text = link.text_en
      if session.language:
        session.languagetext = languagetext_en[session.language]
      if session.level:
        session.leveltext = leveltext_en[session.level]
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

class ObjectImageTransform(common.BaseHandler):
  def get(self, id, w, h):
    key = "img:%s,%s:%s" % (w, h, id)
    cImg = memcache.get(key)
    if cImg is not None:
      self.response.headers['Content-Type'] = 'image/png'
      self.response.out.write(cImg)
      return
    orig = ndb.Key(urlsafe = id).get()
    img = images.Image(orig.image)
    w0 = float(img.width)
    h0 = float(img.height)
    w1 = float(w)
    h1 = float(h)
    resize = False
    maxf = max(w0/w1,h0/h1)
    minf = min(w0/w1,h0/h1)
    maxf = int(maxf*4.)/4.
    minf = int(minf*4.)/4.
    if minf > 1:
      w1 = minf*w1
      h1 = minf*h1
      resize = True
    if maxf < 1:
      w1 = maxf*w1
      h1 = maxf*h1
      resize = True
    x0 = w0/2. - w1/2.
    x1 = w0/2. + w1/2.
    y0 = h0/2. - h1/2.
    y1 = h0/2. + h1/2.
    if w0 < w1:
      x0 = 0
      x1 = w0
    if h0 < h1:
      y0 = 0
      y1 = h0
    img.crop(left_x=x0/w0, top_y=y0/h0, right_x=x1/w0, bottom_y=y1/h0)
    if resize:
      img.resize(width=int(w), height=int(h))
    cImg = img.execute_transforms()
    memcache.add(key, cImg, 3600) 
    self.response.headers['Content-Type'] = 'image/png'
    self.response.out.write(cImg)

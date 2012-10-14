import common
import logging
import settings
from google.appengine.ext import ndb, db
from core import model
from common import with_login, BaseHandler

class EditSession(BaseHandler):
  @with_login
  def get(self, id=None):
    if self.current_user.email not in settings.ADMIN_EMAILS:
      return self.prep_html_response('generic_error.html', { 'code': 401 } )
    # get all speakers (for selecting them)
    speakers = model.Speaker.query().fetch()
    # get all session talks
    sessions = model.SessionTalk.query().fetch()
    # get the session requested
    try:
      session = ndb.Key(urlsafe = id).get()
      is_edit = True
    except:
      session = None
      is_edit = False
    tracks = [ 'Android', 'Java', 'Web', 'Cloud', 'Social', 'Business', 'Workshop' ]
    self.prep_html_response('editsession.html', {'sessions':sessions, 'session':session, 'is_edit':is_edit, 'speakers':speakers, 'tracks':tracks})

  @with_login
  def post(self, id=None):
    if self.current_user.email not in settings.ADMIN_EMAILS:
      return self.prep_html_response('generic_error.html', { 'code': 401 } )
    if id:
      session = ndb.Key(urlsafe = id).get()
    else:
      session = model.SessionTalk()
    session.url = self.request.get('url')
    session.room = self.request.get('room')
    session.slot = self.request.get('slot')
    session.type = self.request.get('type')
    session.title_en = self.request.get('title-en')
    session.title_de = self.request.get('title-de')
    session.abstract_en = self.request.get('abstract-en')
    session.abstract_de = self.request.get('abstract-de')
    if self.request.get('image'):
      session.image = db.Blob(self.request.get('image'))
    session.language = self.request.get('language')
    session.speaker = [ ndb.Key(urlsafe = x) for x in self.request.get_all('speaker') ]
    session.track = self.request.get_all('track')
    # store in DB
    session.put()
    # redirect to the get
    self.redirect("/editsession")

class EditSpeaker(BaseHandler):
  @with_login
  def get(self, id=None):
    if self.current_user.email not in settings.ADMIN_EMAILS:
      return self.prep_html_response('generic_error.html', { 'code': 401 } )
    # get all speakers
    speakers = model.Speaker.query().fetch()
    # get the speaker requested
    try:
      speaker = ndb.Key(urlsafe = id).get()
      is_edit = True
    except:
      speaker = None
      is_edit = False
    self.prep_html_response('editspeaker.html', {'speakers':speakers, 'speaker':speaker, 'is_edit':is_edit})

  @with_login
  def post(self, id=None):
    if self.current_user.email not in settings.ADMIN_EMAILS:
      return self.prep_html_response('generic_error.html', { 'code': 401 } )
    if id:
      speaker = ndb.Key(urlsafe = id).get()
    else:
      speaker = model.Speaker()
    speaker.url = self.request.get('url')
    speaker.name = self.request.get('name')
    speaker.link = self.request.get('link')
    speaker.company = self.request.get('company')
    speaker.company_link = self.request.get('company-link')
    speaker.desc_en = self.request.get('desc-en')
    speaker.desc_de = self.request.get('desc-de')
    speaker.bio_en = self.request.get('bio-en')
    speaker.bio_de = self.request.get('bio-de')
    if self.request.get('image'):
      speaker.image = db.Blob(self.request.get('image'))
    # store in DB
    speaker.put()
    self.redirect("/editspeaker")

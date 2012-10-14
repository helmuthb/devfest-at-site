import common
import logging
import string
from google.appengine.ext import ndb
from core import model
from webapp2_extras import i18n, json

# create a json output usable for Android app
class JsonSessions(common.BaseHandler):
  def get(self):
    events_raw = model.SessionTalk.query().fetch()
    # work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    events = []
    for event_raw in events_raw:
      if event_raw.slot == 'TBD':
        continue
      event = {}
      event['start_date'] = '2012-11-10'
      event['end_date'] = '2012-11-10'
      event['start_time'] = event_raw.slot[:5]
      event['end_time'] = event_raw.slot[-5:]
      event['tags'] = ''
      event['track'] = event_raw.track
      event['attending'] = 'N'
      event['id'] = event_raw.key.urlsafe()
      event['url'] = 'http://www.devfest.at/session/' + event_raw.url
      event['thumbnail_url'] = 'http://www.devfest.at/image/' + event['id']
      event['speaker_id'] = [ sp.urlsafe() for sp in event_raw.speaker ]
      event['room'] = string.lower(event_raw.room)
      event['level'] = 'Intro'
      if locale[0:2] == "de":
        event['title'] = event_raw.title_de
        event['abstract'] = event_raw.abstract_de
      else:
        event['title'] = event_raw.title_en
        event['abstract'] = event_raw.abstract_en
      event['has_streaming'] = False
      event['livestream_url'] = ''
      events.append(event)
    result = { 'result': [ { 'events':events, 'event_type':'sessions' } ] }
    self.response.set_status(200)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.encode(result))

class JsonSpeakers(common.BaseHandler):
  def get(self):
    speakers_raw = model.Speaker.query().fetch()
    # work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    speakers = []
    for speaker_raw in speakers_raw:
      speaker = {}
      if locale[0:2] == "de":
        speaker['bio'] = speaker_raw.bio_de
      else:
        speaker['bio'] = speaker_raw.bio_en
      speaker['first_name'] = ''
      speaker['last_name'] = ''
      speaker['display_name'] = speaker_raw.name
      speaker['user_id'] = speaker_raw.key.urlsafe()
      speaker['thumbnail_url'] = 'http://www.devfest.at/image/' + speaker['user_id']
      speaker['plusone_url'] = speaker_raw.link
      speaker['speaker_id'] = speaker['user_id']
      speakers.append(speaker)
    result = { 'devsite_speakers': speakers }
    self.response.set_status(200)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.encode(result))

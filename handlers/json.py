import common
import logging
from google.appengine.ext import ndb
from core import model
from webapp2_extras import i18n, json

# create a json output usable for Android app
class JsonSessions(common.BaseHandler):
  def get(self):
    events_raw = model.SessionTalk.query().fetch()
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
      event['track'] = []
      event['attending'] = 'N'
      event['id'] = event_raw.key.urlsafe()
      event['speaker_id'] = [ sp.urlsafe() for sp in event_raw.speaker ]
      event['room'] = event_raw.room
      event['level'] = 'Intro'
      event['title'] = event_raw.title_en
      event['has_streaming'] = False
      event['livestream_url'] = ''
      event['abstract'] = event_raw.abstract_en
      events.append(event)
    result = { 'result': [ { 'events':events, 'event_type':'sessions' } ] }
    self.response.set_status(200)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.encode(result))

class JsonSpeakers(common.BaseHandler):
  def get(self):
    speakers_raw = model.Speaker.query().fetch()
    speakers = []
    for speaker_raw in speakers_raw:
      speaker = {}
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

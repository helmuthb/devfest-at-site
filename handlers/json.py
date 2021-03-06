# coding=utf8
import common
import logging
import string
import datetime
import time
import hashlib
from google.appengine.ext import ndb
from core import model
from webapp2_extras import i18n, json

# create a json output usable for Android app
class JsonHandler(common.BaseHandler):
  def get(self):
    # allow work depending on locale
    locale = self.session['locale']
    if self.request.get('locale'):
      locale = self.request.get('locale')
      i18n.get_i18n().set_locale(locale)
    # get the data from the handler
    result = self.getData(locale)
    try:
      result['etag'] = "W/\"" + hashlib.md5(self.__class__.__name__ +
                                        self.etagStamp()).hexdigest() + "\""
    except:
      pass
    self.response.set_status(200)
    # support jsonp
    if self.request.get('callback'):
      self.response.headers['Content-Type'] = 'application/javascript'
      resultText = self.request.get('callback') + "(" + json.encode(result) + ");"
    else:
      self.response.headers['Content-Type'] = 'application/json'
      resultText = json.encode(result)
    self.response.write(resultText)

  # override this method to provide the data
  def getData(self, locale):
    pass

  # helper to get the etag value
  def etagStamp(self):
    return "2012-10-27"

class JsonSessions(JsonHandler):
  def getData(self, locale):
    events_raw = model.SessionTalk.query(model.SessionTalk.event == '2013').fetch()
    events = []
    for event_raw in events_raw:
      if event_raw.slot == 'TBD':
        continue
      event = {}
      if event_raw.type == 'workshop':
        event['start_date'] = '2013-10-18'
      else:
        event['start_date'] = '2013-10-19'
      event['end_date'] = event['start_date']
      event['start_time'] = event_raw.slot[:5]
      event['end_time'] = event_raw.slot[-5:]
      event['tags'] = ''
      event['track'] = event_raw.track
      event['attending'] = 'N'
      event['id'] = event_raw.url
      event['thumbnail_url'] = 'http://www.devfest.at/image/' + event_raw.key.urlsafe()
      event['speaker_id'] = [ sp.urlsafe() for sp in event_raw.speaker ]
      event['room'] = string.lower(event_raw.room)
      if event['room'] == 'ei9':
        event['room'] = 'ei09'
      event['level'] = 'Intro'
      if locale[0:2] == "de":
        event['title'] = event_raw.title_de
        event['abstract'] = event_raw.abstract_de
      else:
        event['title'] = event_raw.title_en
        event['abstract'] = event_raw.abstract_en
      event['has_streaming'] = False
      event['livestream_url'] = ''
      if event_raw.video:
        event['youtube_url'] = [ 'http://youtu.be/' + event_raw.video ]
        event['youtube_link'] = event_raw.video
      
      events.append(event)
    return { 'result': [ { 'events':events, 'event_type':'sessions' } ] }

class JsonSpeakers(JsonHandler):
  def getData(self, locale):
    speakers_raw = model.Speaker.query(model.Speaker.event == '2013').fetch()
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
    return { 'devsite_speakers': speakers }

class JsonNews(JsonHandler):
  def getData(self, locale):
    if locale[0:2] == "de":
      news = [ { 'date': time.mktime(datetime.date(2013, 9, 2).timetuple()),
                 'title': 'Registrierung ist offen',
                 'link': 'https://devfestvienna2013.eventbrite.com',
                 'summary': 'Registrierung ist offen, Eintritt frei!' } ]
    else:
      news = [ { 'date': time.mktime(datetime.date(2013, 9, 2).timetuple()),
                 'title': 'Registration is open',
                 'link': 'https://devfestvienna2013.eventbrite.com',
                 'summary': 'Registration is open, no fee!' } ]
    return { 'announcements': news }

class JsonRooms(JsonHandler):
  def getData(self, locale):
    rooms = [ { 'floor': '0', 'id': 'ws1', 'name': 'WS1' },
              { 'floor': '0', 'id': 'ws2', 'name': 'WS2' },
              { 'floor': '1', 'id': 'ei09', 'name': 'EI9' },
              { 'floor': '1', 'id': 'ei10', 'name': 'EI10' },
              { 'floor': '2', 'id': 'nelsons', 'name': 'Nelson\'s' },
              { 'floor': '3', 'id': 'sektor5', 'name': 'Sektor5' } ]
    if locale[0:2] == 'de':
      rooms.append({ 'floor': '1', 'id': 'mainhall', 'name': 'Vorraum' })
    else:
      rooms.append({ 'floor': '1', 'id': 'mainhall', 'name': 'Main hall' })
    return { 'rooms': rooms }

class JsonSlots(JsonHandler):
  def getData(self, locale):
    if locale[0:2] == "de":
      slots_day0 = [
         { 'start': '13:50', 'end': '14:00', 'meta': 'Vorraum',
            'title': 'Registrierung / Check-In' } ]
      slots_day1 = [
         { 'start': '09:00', 'end': '09:15', 'meta': 'Vorraum',
           'title': 'Registrierung / Check-In' },
         { 'start': '09:15', 'end': '09:30', 'meta': 'Vorraum',
           'title': 'Willkommen & Einführung' },
         { 'start': '12:50', 'end': '13:50', 'meta': 'Vorraum',
           'title': 'Mittagessen' },
         { 'start': '15:35', 'end': '15:50', 'meta': '', 'title': 'Kaffeepause' } ]
      slots_day2 = [
         { 'start': '10:00', 'end': '10:00', 'meta': 'Hauptraum',
           'title': 'Beginn des Android Geburtstags Hackathon' },
         { 'start': '10:00', 'end': '12:30', 'meta': '',
           'title': 'Zeit zum Entwickeln' },
         { 'start': '12:30', 'end': '13:30', 'meta': 'Hauptraum',
           'title': 'Mittagessen' },
         { 'start': '13:30', 'end': '17:30', 'meta': '',
           'title': 'Zeit zum Entwickeln' },
         { 'start': '17:30', 'end': '18:30', 'meta': 'Hauptraum',
           'title': 'Vorstellung der Ergebnisse' },
         { 'start': '18:30', 'end': '19:00', 'meta': 'Hauptraum',
           'title': 'Preisverleihung' } ]
    else:
      slots_day0 = [
         { 'start': '13:50', 'end': '14:00', 'meta': 'Main Hall',
            'title': 'Registration / Check-In' } ]
      slots_day1 = [
         { 'start': '09:00', 'end': '09:15', 'meta': 'Main Hall',
           'title': 'Registration / Check-In' },
         { 'start': '09:15', 'end': '09:30', 'meta': 'Main Hall',
           'title': 'Welcome & Introduction' },
         { 'start': '12:50', 'end': '13:50', 'meta': 'Main Hall',
           'title': 'Lunch Break' },
         { 'start': '15:35', 'end': '15:50', 'meta': '', 'title': 'Break' } ]
      slots_day2 = [
         { 'start': '10:00', 'end': '10:00', 'meta': 'Main room',
           'title': 'Start of Android Birthday Hackathon' },
         { 'start': '10:00', 'end': '12:30', 'meta': '',
           'title': 'Time for developing' },
         { 'start': '12:30', 'end': '13:30', 'meta': 'Main room',
           'title': 'Lunch Break' },
         { 'start': '13:30', 'end': '17:30', 'meta': '',
           'title': 'Time for developing' },
         { 'start': '17:30', 'end': '18:30', 'meta': 'Main room',
           'title': 'Presentation of Results' },
         { 'start': '18:30', 'end': '19:00', 'meta': 'Main room',
           'title': 'Award Ceremony' } ]
    return { 'day': [ { 'date': '2013-10-18', 'slot': slots_day0 },
                      { 'date': '2013-10-19', 'slot': slots_day1 },
                      { 'date': '2013-10-20', 'slot': slots_day2 } ] }

class JsonTracks(JsonHandler):
  def getData(self, locale):
    if locale[0:2] == 'de':
      tracks = [
         { 'color': '#A6BC40', 'name': 'Android',
           'abstract': 'Lerne Anwendungen (Apps) für Handys und Tablets ' +
                       'unter Android zu entwickeln' },
         { 'color': '#76BC20', 'name': 'Social',
           'abstract': 'Netzwerke wie Google+, Twitter oder Facebook sowie ' +
                       'deren Einbindung in eigene Anwendungen' },
         { 'color': '#2076BC', 'name': 'Cloud', 'abstract': '' },
         { 'color': '#E4388F', 'name': 'Hackathon', 'abstract': '' },
         { 'color': '#97B0DA', 'name': 'Business', 'abstract': '' },
         { 'color': '#DC4E30', 'name': 'Web', 'abstract': '' },
         { 'color': '#A1609D', 'name': 'Workshop',
           'abstract': 'Mit einem Workshop machst du die ersten Schritte ' +
                       'in einer neuen Technologie unter guter Führung.' } ]
    else:
      tracks = [
         { 'color': '#A6BC40', 'name': 'Android',
           'abstract': 'Learn about developing mobile handset and tablet ' +
                       'apps for Android' },
         { 'color': '#76BC20', 'name': 'Social',
           'abstract': 'Social networks like Google+, Twitter or Facebook ' +
                       'and how you can include them into your applications' },
         { 'color': '#2076BC', 'name': 'Cloud', 'abstract': '' },
         { 'color': '#E4388F', 'name': 'Hackathon', 'abstract': '' },
         { 'color': '#97B0DA', 'name': 'Business', 'abstract': '' },
         { 'color': '#DC4E30', 'name': 'Web', 'abstract': '' },
         { 'color': '#A1609D', 'name': 'Workshop',
           'abstract': 'Hands-on workshops which help you making the first ' +
                       'steps with a new technology' } ]
    return { 'track': tracks }

class JsonSuggests(JsonHandler):
  def getData(self, locale):
    return { 'words': [] }

class JsonSponsors(JsonHandler):
  def getData(self, locale):
    return [
      { 'website': 'http://www.cenarion.com/', 'procuct_pod': 'Web',
        'company_description': 'Better software for a better world - ' +
             'Cenarion Information Systems is a leader in innovative ' +
             'software solutions.',
        'logo_img': 'http://www.cenarion.com/sites/default/files/cenarion-png-24-200.png',
        'company_name': 'Cenarion' } ]

import common
import logging
from core import model

from google.appengine.ext import db

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

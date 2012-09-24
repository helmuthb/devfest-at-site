import common
import logging
from core import model

from google.appengine.ext import db

class CallForSpeakers(common.BaseHandler):
  @common.with_login
  def get(self):
    self.prep_html_response('call.html') 

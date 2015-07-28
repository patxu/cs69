from parse_rest.connection import register
from parse_rest.datatypes import Object

APP_ID = "JRZP6EKCJAPCElSMEetXj2duLFU2Cl3U14x8mfUU"
REST_API_KEY = "mCpEIYFAgDR7QlMCyIV7PCCzzPlD80P2gOmi1gma"

register(APP_ID, REST_API_KEY, master_key=None)

class Reading(Object):
  pass

readingObj = Object()
readingObj = Object.factory("Reading")
readingObj = Reading(distance = 26.12459381099)
readingObj.save()

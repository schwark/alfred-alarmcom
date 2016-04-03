import string
from binascii import hexlify, unhexlify
import json
from pyalarmdotcom import Alarmdotcom
from simplecrypt import encrypt, decrypt
from alfred import Feedback
from keychain import Keychain
from os import getlogin

DB_FILE = 'creds.json'
KEYCHAIN = 'login'
SERVICE_NAME = 'com.alfred.satyavolu.alarm.com'
JOIN_STRING = '....'

def update_creds(query=""):
    query = query.strip()
    parts = query.split(' ')
    if (len(parts) > 1):
      username = parts[0]
      password = parts[1]
      crypto = len(parts) > 2 and parts[2] or ''
      success, message = save_db({'username': username, 'password': password}, crypto)
      return message

def save_db(creds, password=''):
  creds['password'] = password and hexlify(encrypt(password, creds['password'])) or creds['password']
  creds['username'] = password and hexlify(encrypt(password, creds['username'])) or creds['username']
  keychain = Keychain()
  account = getlogin()
  password = "%s%s%s" % (creds['username'], JOIN_STRING, creds['password'])
  return keychain.set_generic_password(KEYCHAIN, account, password, SERVICE_NAME)

def load_db(password=''):
  creds = {}
  keychain = Keychain()
  account = getlogin()
  payload = keychain.get_generic_password(KEYCHAIN, account, SERVICE_NAME)
  if payload and 'password' in payload:
    parts = payload['password'].split(JOIN_STRING)
    if(len(parts) > 1):
      creds['password'] = password and decrypt(password, unhexlify(parts[1])) or parts[1]
      creds['username'] = password and decrypt(password, unhexlify(parts[0])) or parts[0]
  return creds

def get_alarm(password=''):
    creds = load_db(password)
    return Alarmdotcom(creds['username'], creds['password'])

def execute_command(command=""):
    command = command.lower().strip()
    parts = command.split(' ')
    message = "Command failed"
    password = len(parts) > 1 and parts[1] or ''
    command = parts[0]
    alarm = get_alarm(password)
    if "off" == command:
        alarm.disarm()
        message = "Alarm disarmed"
    elif "stay" == command:
        alarm.arm_stay()
        message = "Alarm armed to Stay"
    elif "away" == command:
        alarm.arm_away()
        message = "Alarm armed to Away"
    return message

def list_collector(query=""):
    feedback = Feedback()
    query = query.lower().strip()
    parts = query.split(' ')
    password = len(parts) > 1 and parts[1] or ''
    query = parts[0].strip()
    if not query or "stay".startswith(query):
      feedback.addItem(title="Stay", subtitle="Arm in Stay mode", arg="stay "+password, valid=True, autocomplete="Stay "+password)
    if not query or "away".startswith(query):
      feedback.addItem(title="Away", subtitle="Arm in Away mode", arg="away "+password, valid=True, autocomplete="Away "+password)
    if not query or "off".startswith(query):
      feedback.addItem(title="Off", subtitle="Disarm the Alarm", arg="off "+password, valid=True, autocomplete=" Off "+password)
    
    return feedback


def main():
    print update_creds('testing')

if __name__ == "__main__":
    main()


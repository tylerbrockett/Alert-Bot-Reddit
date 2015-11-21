import time
import atexit
import sys
import os
from utils import colors

i = None
is_running = True
check_interval = 2 # interval between checks

def handle_bot_not_running():
    global is_running, check_interval
    print 'BOT NOT RUNNING'
    if is_running:
        print colors.FORE_RED + 'SWITCH TO FALSE' + colors.FORE_RESET
        is_running = False
        check_interval = 10


def handle_bot_is_running():
    global is_running, check_interval
    print 'Everything is good. Carry on sir.'
    if not is_running:
        print colors.FORE_GREEN + 'SWITCH TO TRUE' + colors.FORE_RESET
        is_running = True
        check_interval = 2


def check_on_bot():
    print 'Checking...'
    with open(os.getcwd() + '/bot/monitoring/process_id.pid', 'r') as f:
        contents = f.read()
        f.close()
        if contents == '':
            print 'PID: EMPTY'
            handle_bot_not_running()
        else:
            print 'PID: ', contents
            handle_bot_is_running()
    print '\n'


def main():
    global i
    i = 0
    while True:
        time.sleep(check_interval)
        i += 1
        print 'ITERATION', i
        check_on_bot()


def exit_handler():
    print 'EXITING'



__author__ = 'tyler'
if __name__ == "__main__":
    atexit.register(exit_handler)
    main()






















"""Send an email message from the user's account.
"""
'''
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.b64encode(message.as_string())}


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.b64encode(message.as_string())}

'''



#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/net/smtpemail.py
# author: Tim Wang
# date: Jan., 2014

""" class Email define SMTP connect and sender info.
    writemail make a email message which can be send by Email
"""

import os.path
import smtplib
import mimetypes
from email import encoders
from email.utils import formatdate
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def _dict_lowerkey(dictvar):
    """change dict's iter key to lower
    """
    for k, v in dictvar.iteritems():
        if isinstance(k, (str, unicode)):
            k = k.lower()
        yield k, v


class Smtp:
    
    """SMTP and sender define
    """
    def __init__(self, **kwg):
        """init setting include smpt server/port 
                (the server should be provided)
            and sender "from" address
        """
        self._setting = dict(kwg)
        self._smtpserver = smtplib.SMTP()
        try:
            statue = self._smtpserver.connect(
                self._setting.get('server'),
                self._setting.get('port', 25)
                )[0]
            self.statue = ('fail', 'connected')[statue == 220]
        except smtplib.SMTPConnectError:
            self.statue = 'fail'

    def __del__(self):
        self._smtpserver.quit()
    
    def login(self, authenticatename=None, authenticatepwd=None):
        """manual authenticate with arguments or self._setting
        """
        pwd = authenticatepwd or self._setting.get("Pwd")
        name = authenticatename or self._setting.get("From")
        if pwd:
            try:
                self._smtpserver.helo()
                self.statue = ('logon', 'fail')[
                    self._smtpserver.login(name, pwd)[0] == 235
                    ]
            except smtplib.SMTPAuthenticationError:
                self.statue = 'fail'

    def send(self, msg):
        """send msg by setting's smtp server
        """
        if self.statue == 'fail':
            return
        msg["From"] = msg.get("From", self._setting.get("From")) 
        self._smtpserver.sendmail(
            msg['From'],
            msg['To'].split(',')+
            msg['Cc'].split(','),
            msg.as_string()
            )


def _attach_text(file_name, subtype):
    """inner function to attach text file
    """
    with open(file_name) as handle:
        return MIMEText(handle.read(), _subtype=subtype)

def _attach_image(file_name, subtype):
    """inner function to attach image file
    """
    with open(file_name, 'rb') as handle:
        return MIMEImage(handle.read(), _subtype=subtype)

def _attach_audio(file_name, subtype):
    """inner function to attach audio file
    """
    with open(file_name, 'rb') as handle:
        return MIMEAudio(handle.read(), _subtype=subtype)

def _attach(file_name, maintype, subtype):
    """inner function to attach file
    """
    with open(file_name, 'rb') as handle:
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(handle.read())
        encoders.encode_base64(file_msg)
        return file_msg


ATTACH_SWITCHER = {
    'text': _attach_text,
    'image': _attach_image,
    'audio': _attach_audio,
    }


def attach(msg, file_name):
    """attach a file to the message package:msg
    """
    ctype, encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed),
        # so use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    attach_proc = ATTACH_SWITCHER.get(maintype)
    if not attach_proc:
        file_msg = _attach(file_name, maintype, subtype)
    else:
        file_msg = attach_proc(file_name, subtype)
    # Set the filename parameter
    file_msg.add_header('Content-Disposition', 'attachment', 
        filename=os.path.split(file_name)[-1])
    msg.attach(file_msg)
    return msg


def writemail(coding='utf-8', **kwg):
    """write a email message
    """
    setting = dict(_dict_lowerkey(kwg))
    msg = MIMEMultipart()
    msg["To"] = setting.get('to', 'me@example.com')
    msg["Cc"] = setting.get('cc', '')
    msg['Date'] = formatdate()
    msg["Subject"] = Header(setting.get('subject', 'No Subject'), coding)
    if "html" in setting:
        msg.attach(MIMEText(
            setting.get('html').encode(coding), 
            'html', 
            _charset=coding
            ))
    if "context" in setting:
        msg.attach(MIMEText(
            setting.get('context').encode(coding), 
            'plain', 
            _charset=coding
            ))
    
    attaches = setting.get('attach') or setting.get('files') 
    if not attaches:
        return msg
    if isinstance(attaches, (str, unicode)):
        attaches = [attaches]
    if isinstance(attaches, (list, tuple)):
        return reduce(attach, [filename for filename in attaches 
                if os.path.isfile(filename)], 
            msg)
    else:
        return msg


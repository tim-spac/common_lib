#!/usr/bin/env python
# encoding: utf-8
#
# filename: common_lib/net/sendemail.py
#

""" class Email define SMTP connect and sender info.
    writemail make a email message which can be send by Email
"""

import os.path
import smtplib
from email import encoders
from email.utils import formatdate
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import mimetypes


class Email:
    
    """SMTP and sender define
    """
    def __init__(self, **kwg):
        """init setting include smpt server/port 
            and sender "from" address
        """
        self._setting = dict(kwg)

    def send(self, msg):
        """send msg by setting's smtp server
        """
        smtp = smtplib.SMTP()
        sender = self._setting.get("From")
        pwd = self._setting.get("Pwd")
        smtp.connect(
            self._setting.get('server'),
            self._setting.get('port', 25)
            )
        if pwd:
            smtp.login(sender, pwd)
        msg["From"] = msg.get("From", sender) 
        smtp.sendmail(
            msg['From'],
            msg['To'].split(',')+
            msg['Cc'].split(','),
            msg.as_string()
            )
        smtp.quit()


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


attach_switcher = {
    'text': _attach_text,
    'image': _attach_image,
    'audio': _attach_audio,
    }


def attach(msg, file_name):
    """attach a file to the message package:msg
    """
    ctype, encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    attach_proc = attach_switcher.get(maintype)
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
    msg = MIMEMultipart()
    msg["To"] = kwg.get('To', 'me@example.com')
    msg["Cc"] = kwg.get('Cc', '')
    msg['Date'] = formatdate()
    msg["Subject"] = Header(kwg.get('Subject', 'No Subject'), coding)
    if "Html" in kwg:
        msg.attach(MIMEText(
            kwg.get('Html').encode(coding), 
            'html', 
            _charset=coding
            ))
    if "Context" in kwg:
        msg.attach(MIMEText(
            kwg.get('Context').encode(coding), 
            'plain', 
            _charset=coding
            ))
    
    attaches = kwg.get('attach')
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


if __name__ == "__main__":
    email = Email(
        server="smtp.163.com",
        From='tim_spac@163.com',
        Pwd='xxxx',
        )
    email.send(writemail(
            To="tim_spac@163.com",
            Subject=u"邮件主题",
            Context=u"""这里是邮件正文.""",
            attach=[
                'sendmail.py',
                r'~/images/Bing/EurasianRed_ZH-CN11954213173_1366x768.jpg',
                r'~/music/21 - Adele/01.Rolling in the deep.mp3',
                ],
            ))

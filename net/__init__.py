#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/net/__init__.py
# author: Tim Wang
# date: Jan., 2014


"""common_lib/net
    is for network tools
        "smtpemail" include:
            "Smtp" class for define SMTP connection, and send methord
            "writemail" make an email message
            "attach" for attach file(s) to an email message
"""

from common_lib.net.smtpemail import Smtp
from common_lib.net.smtpemail import writemail
from common_lib.net.smtpemail import attach
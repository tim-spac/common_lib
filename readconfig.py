#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/readconfig.py
# author: Tim Wang
# date: Jan., 2014

"""module for read config file
"""

import yaml
import codecs
import ConfigParser as configparser


def readini(configfile):
    """read the INI file config"""
    parser = configparser.SafeConfigParser()
    parser.read(configfile)
    return dict([(sec, dict(parser.items(sec)))
            for sec in parser.sections()])


def readyaml(configfile):
    """read the YAML file config"""
    return yaml.load(codecs.open(configfile, 'r', 'utf-8'))

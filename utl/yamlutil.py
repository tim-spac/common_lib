#!/usr/bin/env python
# coding: utf-8
#
# author: Tim Wang
# date: May, 2014
# filename: yamlutil.py

import yaml


def store2yaml(data, ymlfile, coding='utf-8'):
    yaml.safe_dump(data, open(ymlfile, 'wt'),
        indent=4, 
        allow_unicode=True,
        encoding=coding,
        )
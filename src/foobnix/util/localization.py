#-*- coding: utf-8 -*-
'''
Created on 24  2010

@author: ivan
'''
import gettext

def foobnix_localization():
    APP_NAME = "foobnix"
    gettext.install(APP_NAME, unicode=True)
    gettext.textdomain(APP_NAME)


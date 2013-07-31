#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import unicodedata
from xml.etree.ElementTree import fromstring
from HTMLParser import HTMLParser

from Feedback import Feedback


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


KEY = 'CHANGE ME'
length = 25

def shoplist(query):
    query = query.decode('utf-8')
    query = unicodedata.normalize('NFC', query)

    encoded = urllib.urlencode({'query':query.encode('utf-8')})
    url = 'http://openapi.naver.com/search?{}&display={}&start=1&target=shop&sort=sim&key={}'.format(encoded, length, KEY)
    response = urllib2.urlopen(url)
    r = response.read()
    t = fromstring(r)

    items = t.findall('channel/item')

    fb = Feedback()

    for i in items:
        title = strip_tags(i.find('title').text)
        url = i.find('link').text
        price = i.find('lprice').text
        fb.add_item(title, subtitle=u"₩ {:,}".format(int(price)), arg=url)

    print fb

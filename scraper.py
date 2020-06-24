#!/usr/bin/env python
import requests
from lxml import html
from sys import argv

def scraper(url, xpathKey):
     page = requests.get(url)
     tree = html.fromstring(page.content)
     return [i.text.strip() for i in tree.xpath(xpathKey)]

print scraper(argv[1], argv[2])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 9 football"""
from bs4 import BeautifulSoup
import urllib2

URL = 'http://www.cbssports.com/nfl/stats/playersort/nfl/year-2016-season-regular-category-touchdowns'

TABLE_ELT = 'table.data'
TABLE_HEADERS_ELT = 'tr[class$=label]'
TABLE_ROW_ELT = 'tr[class^=row]'

FIELDS = ['Player', 'Pos', 'Team', 'TD']
TOP = 20

def getFieldContent(field):
	for child in field.children:
		if hasattr(child, 'string'):
			return unicode(child.string)

		if len(list(child.children)) > 1:
			return getFieldContent(child)
		else:
			for content in child.children:
				return content
	
def getFieldsIndex(headers):
	res = dict()

	for (i, header) in enumerate(headers.children):
		header_name = getFieldContent(header)
		if header_name in FIELDS:
			res[i] = header_name

	return res

if __name__ == '__main__':
	webpage = urllib2.urlopen(URL)
	page = BeautifulSoup(webpage.read(), 'html.parser')

	table = page.select_one(TABLE_ELT)
	headers = table.select_one(TABLE_HEADERS_ELT)
	
	fields_index = getFieldsIndex(headers)
	indexes = fields_index.keys()
	
	players = table.select(TABLE_ROW_ELT)

	res = list()
	for (i, player) in enumerate(players):
		if i == TOP:
			break
		player_metadata = dict()
		for (j, content) in enumerate(player.children):
			if j not in indexes:
				continue
			player_metadata[fields_index[j]] = getFieldContent(content)
		res.append(player_metadata)

	print res
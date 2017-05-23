#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 9 football"""
from bs4 import BeautifulSoup
import urllib2

URL = 'https://finance.yahoo.com/quote/AAPL/history?ltr=1'

TABLE_ELT = 'table[data-reactid="34"]'
TABLE_HEADERS_ELT = 'tr[data-reactid="36"]'
TABLE_ROW_ELT = 'tbody[data-reactid="51"]'

FIELDS = ['Date', 'Close']
TOP = -1

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
	
	rows = table.select_one(TABLE_ROW_ELT).children

	res = list()
	for (i, data) in enumerate(rows):
		if i == TOP:
			break
		row_metadata = dict()
		for (j, content) in enumerate(data.children):
			if j not in indexes:
				continue
			row_metadata[fields_index[j]] = getFieldContent(content)

		if len(row_metadata.values()) == len(indexes):
			res.append(row_metadata)

	print res
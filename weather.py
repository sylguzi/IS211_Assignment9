#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 9 football"""
from bs4 import BeautifulSoup
import urllib2

URL = 'https://www.wunderground.com/history/airport/KNYC/2015/1/11/MonthlyHistory.html'

TABLE_ELT = 'table[id="obsTable"]'
TABLE_ROWS_ELT = 'tbody'

TODAY = 11

SKIP_HEADERS = 0

PREDICTED = 'predicted'
ACTUAL = 'actual'

FIELDS_INDEX = {0: 'day', 1: 'high', 2: 'avg', 3: 'low'}
FIELDS_INDEX_LEN = len(FIELDS_INDEX)

def getFieldContent(field):
	if hasattr(field, 'string'):
		return unicode(field.string)

	for child in field.children:
		if len(list(child.children)) > 1:
			return getFieldContent(child)
		else:
			for content in child.children:
				return content

if __name__ == '__main__':
	webpage = urllib2.urlopen(URL)
	page = BeautifulSoup(webpage.read(), 'html.parser')

	table = page.select_one(TABLE_ELT)
	rows = table.select(TABLE_ROWS_ELT)

	res = {PREDICTED: list(), ACTUAL: list()}
	for (i, data) in enumerate(rows):
		if i == SKIP_HEADERS:
			continue
		row_metadata = dict()
		select_cells = data.select('td')
		for (j, content) in enumerate(select_cells):
			if j >= FIELDS_INDEX_LEN:
				break
			aContent = content.find('a')
			spanContent = content.find('span')
			row_metadata[FIELDS_INDEX[j]] = getFieldContent(aContent) if aContent is not None else getFieldContent(spanContent)
		if len(row_metadata.values()) == FIELDS_INDEX_LEN:
			if i <= TODAY:
				res[ACTUAL].append(row_metadata)
			else:
				res[PREDICTED].append(row_metadata)

	print res
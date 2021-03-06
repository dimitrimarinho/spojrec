# -*- coding: utf-8 -*-
import sys
from lxml.html import parse
from lxml.html import tostring
from urllib2 import urlopen

from constants import SPOJ_URLS
from crawler.dataExtractor.extractor import extract_problem_data, extract_user_data, extract_submissions_data
from crawler.dataExtractor.signedlistParser import parseSignedlist

def _raw_fetch(url):
	print >>sys.stderr, url
	page = urlopen(url)
	html = parse(page).getroot()
	return html


def _fetch_user_statistics(spojId, contest, database):
	url = SPOJ_URLS[contest] + '/users/' + spojId
	html = _raw_fetch(url)
	item = extract_user_data(html)
	if item['_id'] == spojId:
		database.update_user(dict(item))	
	
	
def _fetch_user_problems(spojId, contest, database):
	url = SPOJ_URLS[contest] + '/status/' + spojId + '/signedlist/'
	html = tostring(_raw_fetch(url))
	item = extract_submissions_data(spojId, html)
	parsedProblems = parseSignedlist(item['data'])
	if len(parsedProblems) > 0:
		database.update_submission_data(dict(item))
	
	
def fetch_user(spojId, contest, database, onlySubmitions=False):
	if not onlySubmitions:
		_fetch_user_statistics(spojId, contest, database)
	_fetch_user_problems(spojId, contest, database)
	

def fetch_problem(spojId, contest, database):
	url = SPOJ_URLS[contest] + '/problems/' + spojId
	html = _raw_fetch(url)
	item = extract_problem_data(html, url)
	database.update_problem(dict(item))
	
	

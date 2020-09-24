# -*- coding: utf-8 -*-

import re
try:
	from hashlib import md5
except:
	from md5 import md5
from random import randint
#import struct

import time
from urllib import unquote, quote


VERSION = "4.4sh"
COOKIE_NAME = "__utmmobile"
COOKIE_PATH = "/"
COOKIE_USER_PERSISTENCE = 11
DOMAIN = "polbox.tv"
UATRACK = "UA-79652556-7"
IP_LOOKUP_SERVICE = "http://dynupdate.no-ip.com/ip.php"

def get_ip(remote_address):
	# dbgMsg("remote_address: " + str(remote_address))
	if not remote_address:
		return ""
	matches = re.match('^([^.]+\.[^.]+\.[^.]+\.).*', remote_address)
	if matches:
		return matches.groups()[0] + "0"
	else:
		return ""

def get_visitor_id(guid, cookie):
	if cookie:
		return cookie
	message = ""
	# Create the visitor id using the guid.
	message = guid + UATRACK

	md5String = md5(message).hexdigest()
	return "0x" + md5String[:16]

def get_random_number():
	return str(randint(0, 0x7fffffff))

def send_request_to_google_analytics(utm_url, ua):
	import urllib2
	try:
		req = urllib2.Request(utm_url, None,
									{'User-Agent':ua}
									 )
		response = urllib2.urlopen(req).read()
	except:
		print ("GA fail: %s" % utm_url)
	return response

def track_page_view(visitor_id, path, ua, extra):
	domain = DOMAIN

	document_path = unquote(path)

	utm_gif_location = "http://www.google-analytics.com/__utm.gif"

	import urllib
	ip = urllib.urlopen(IP_LOOKUP_SERVICE).read()

	# // Construct the gif hit url.
	utm_url = utm_gif_location + "?" + \
			"utmwv=" + VERSION + \
			"&utmn=" + get_random_number() + \
			"&utmhn=" + quote(domain) + \
			"&utmsr=" + quote(extra.get("screen", "")) + \
			"&utme="+ \
			"&utmr=" + quote('-') + \
			"&utmp=" + quote(document_path) + \
			"&utmac=" + UATRACK + \
			"&utmcc=__utma%3D999.999.999.999.999.1%3B" + \
			"&utmvid=" + visitor_id + \
			"&utmip=" + get_ip(ip)
	# dbgMsg("utm_url: " + utm_url)
	print "Analitycs: %s" % utm_url
	return send_request_to_google_analytics(utm_url, ua)

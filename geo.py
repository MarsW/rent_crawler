# encoding: utf-8

import urllib2,urllib
from lxml import etree
import re
import json

def get_location(address):
	url = "http://maps.googleapis.com/maps/api/geocode/json?address="+address
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	html = response.read()
	data = json.loads(html)

	try:
		lat = data['results'][0]['geometry']['location']['lat']
	except:
		lat=""

	try:
		lng = data['results'][0]['geometry']['location']['lng']
	except:
		lng=""
	
	return str(lat)+","+str(lng)

def get_duration11(address):
	
	url_marsw = "http://maps.googleapis.com/maps/api/directions/json?origin="+address+"&destination=台北市中山區松江路63巷7-1號&sensor=false&mode=driving&avoid=highways&language=zh-tw"
	req = urllib2.Request(url_marsw)
	response = urllib2.urlopen(req)
	html = response.read()
	data = json.loads(html)

	duration_marsw = ""
	try:
		duration_marsw = data['routes'][0]['legs'][0]['duration']['text']
	except:
		duration_marsw = get_duration1(address)

	return duration_marsw

def get_duration12(address):
	
	url_awoo = "http://maps.googleapis.com/maps/api/directions/json?origin="+address+"&destination=中央研究院&sensor=false&mode=driving&avoid=highways&language=zh-tw"
	req = urllib2.Request(url_awoo)
	response = urllib2.urlopen(req)
	html = response.read()
	data = json.loads(html)
	
	duration_awoo = ""
	try:
		duration_awoo = data['routes'][0]['legs'][0]['duration']['text']
	except:
		duration_awoo = get_duration2(address)
	return duration_awoo

def get_duration13(address):
	url_akoung = "http://maps.googleapis.com/maps/api/directions/json?origin="+address+"&destination=新店區寶橋路235巷129號&sensor=false&mode=transit&language=zh-tw"
	req = urllib2.Request(url_akoung)
	response = urllib2.urlopen(req)
	html = response.read()
	data = json.loads(html)

	duration_akoung = ""
	try:
		temp = data['routes'][0]['legs'][0]
		duration_akoung = temp['duration']['text']+','+temp['steps'][0]['html_instructions']+temp['steps'][0]['duration']['text']
	except:
		duration_akoung = get_duration3(address)

	return duration_akoung

def get_duration1(address):
	url_marsw = "http://maps.google.com/?saddr="+address+"&daddr=台北市中山區松江路63巷7-1號&dirflg=h&hl=zh-tw"
	req = urllib2.Request(url_marsw)
	req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
	try:
		response = urllib2.urlopen(req)
	except:
		return ""
	html = response.read()

	duration_marsw = ""
	try:
		duration_marsw = html.split('[[0,\\\"')[1].split("分\\\"")[0].split("\\\"")[-1]+"分"
		print duration_marsw
	except:
		duration_marsw = ""
		print url_marsw
	return duration_marsw

def get_duration2(address):
	url_awoo = "http://maps.google.com/?saddr="+address+"&daddr=中央研究院&dirflg=h&hl=zh-tw"
	req = urllib2.Request(url_awoo)
	req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
	try:
		response = urllib2.urlopen(req)
	except:
		return ""
	html = response.read()

	duration_awoo = ""
	try:
		duration_awoo = html.split('[[0,\\\"')[1].split("分\\\"")[0].split("\\\"")[-1]+"分"
		print duration_awoo
	except:
		duration_awoo = ""
		print url_awoo
	return duration_awoo

def get_duration3(address):
	url_akoung = "http://maps.google.com/maps?saddr="+address+"&daddr=新店區寶橋路235巷129號&dirflg=rS&hl=zh-tw"
	req = urllib2.Request(url_akoung)
	req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
	try:
		response = urllib2.urlopen(req)
	except:
		return ""
	html = response.read()

	duration_akoung = ""
	try:
		duration_akoung = html.split('[[3,\\\"')[1].split("分\\\"")[0].split("\\\"")[-1]+"分"
		print duration_akoung
	except:
		duration_akoung = ""
		print url_akoung
	return duration_akoung
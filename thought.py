
# Location
#import spacy
#nlp = spacy.load('en')

# Get location deets

import pandas as pd
import numpy as np
import re
from collections import Counter

# Locations
df = pd.read_csv('us_cities_states_counties.csv', delimiter="|")
locs = []
locs.extend(df['City'].str.title().unique())
locs.extend(df['State full'].str.title().unique())
locs.extend(df['County'].str.title().unique())

# Time
import parsedatetime
cal = parsedatetime.Calendar()
from datetime import datetime
from timex import tag_time

# Yahoo Weather API
import urllib2, urllib, json
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\")"

# Google Places API
google_api = "super secret"
goog_query = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# Our database of activities
activities_list = json.load(open('list.json'))['all']
activities_keys = activities_list.keys()

# Messages

greetings = ['hey', 'hello', 'what\'s up', 'hi']
gratitudes = ['thanks', 'thank you']
resets = ['stop', 'reset', 'cancel']

import random
intros = [ 'Wow, that sounds fun!', 'Interesting...' ]

# initalize global vars
global complete_input
global processed
global current_data
complete_input = ""
processed = { 'time': False, 'location': False, 'activities': False }
current_data = { 'time': None, 'location': None, 'activities': [] }

##### PARSE INPUT #####

def get_time(phrase):
	time_expr = tag_time(phrase)
	if time_expr == 'no time found':
		return None
	else:
		# Convert time expression into numerical time
		time_struct, parse_status = cal.parse(time_expr)
		time = datetime(*time_struct[:3])
		# Make sure time is present or future, not past
		if datetime.now() <= time:
			return { 'time': time, 'time_expr': time_expr }
		else: return None

def get_location(phrase):
	"""
	doc = nlp(phrase, "utf-8")
	for ent in doc.ents:
		if ent.label_ == 'GPE':
			print(ent.text)
			return str(ent.text)
	return None
	"""
	locs_found = []
	formatted_phrase = phrase.title()
	for loc in locs:
		if str(loc) in formatted_phrase:
			locs_found.append(str(loc))
	if len(locs_found) == 0:
		return None
	else:
		loc_counter = Counter(locs_found)
		most_common = loc_counter.most_common(1)[0][0]
		return most_common


def get_activities(phrase):
	activities = []
	for key in activities_keys:
		if key in phrase:
			activities.append(key)
	return activities

##### GET DATA #####

def get_list(data):
	things = []
	# Based on activities
	for activity in data['activities']:
		things.extend(activities_list[activity])
	return list(set(things))

def get_weather(location, data_time):
	# Convert date to format for Yahoo API
	time = data_time.strftime('%d %b %Y')
	# Get weather conditions for the day - note weather conditions do not go more than a month
	yql_url = baseurl + urllib.urlencode({ 'q': (yql_query % location) }) + "&format=json"
	result = urllib2.urlopen(yql_url).read()
	json_result = json.loads(result)
	if json_result['query']['count'] != 0:
		weather_data = json_result['query']['results']['channel']['item']['forecast']
		weather = next((item['text'] for item in weather_data if item['date'] == time), None)
		return weather
	else: return None

def get_points_of_interest(place):
	req = goog_query + urllib.urlencode({ 'query': 'attractions in ' + place, 'key': google_api })
	print(req)
	result = json.loads(urllib2.urlopen(req).read())
	points = [interest['name'] for interest in result['results']][0:2] # only first 2
	return points

##### CREATE RESPONSE #####

def parse_phrase(input_text):

	# Try to extract missing data if its not there
	if current_data['time'] == None:
		current_data['time'] = get_time(input_text)
	if current_data['location'] == None:
		current_data['location'] = get_location(input_text)
	if len(current_data['activities']) == 0:
		current_data['activities'] = get_activities(input_text.lower())

	response = ""

	# Generate response
	if current_data['time'] != None and current_data['location'] != None and not processed['time'] and not processed['location']:
		weather = get_weather(current_data['location'], current_data['time']['time'])
		if weather:
			response += ' The weather is ' + weather + ' in ' + current_data['location'] + ' ' + current_data['time']['time_expr'] + '.'
		response += 'Maybe you could check out ' + ' and '.join(get_points_of_interest(current_data['location']))
		# todo: respond with what clothing to wear
		processed['time'] = True
		processed['location'] = True
	if len(current_data['activities']) > 0:
		response += ' Seems like you\'ve got some things to pack!'
		response += ' You definitely want to pack a ' + ', '.join(get_list(current_data)[:5])

	response = response.strip()
	print(response)

	# Render formatted HTML
	render_this = str(complete_input)

	if current_data['time'] != None:
		render_this = render_this.replace(current_data['time']['time_expr'], 
			"<span style=\"color: #f18973;\">%s</span>" % current_data['time']['time_expr'])
	if current_data['location'] != None:
		render_this = render_this.replace(current_data['location'], 
			"<span style=\"color: #00FF00;\">%s</span>" % current_data['location'])
	if len(current_data['activities']) != 0:
		for activity in current_data['activities']:
			render_this = render_this.replace(activity,  
				"<span style=\"color: #0000FF;\">%s</span>" % activity)

	return response, render_this

##### ENTRY AND EXIT POINT #####

def converse(input_chunk):
	global current_data
	global complete_input
	global processed

	if any(greeting in input_chunk.lower().split() for greeting in greetings):
		return 'Hi there! What can I help you with?', ""
	elif any(gratitude in input_chunk.lower() for gratitude in gratitudes):
		# resets after gratitude expressed
		current_data = { 'time': None, 'location': None, 'activities': [] }
		complete_input = ""
		processed = { 'time': False, 'location': False, 'activities': False }
		return 'No problem!', ""
	elif any(reset in input_chunk.lower() for reset in resets):
		# resets after cancellation
		current_data = { 'time': None, 'location': None, 'activities': [] }
		complete_input = ""
		processed = { 'time': False, 'location': False, 'activities': False }
		return 'Cancelled', ""
	else:
		complete_input = complete_input + input_chunk
		return parse_phrase(input_chunk)

# END

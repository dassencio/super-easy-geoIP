#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import pickle

from config import *
from ipfunctions import *


# class which holds geolocation data for an IP address
class IPInfo:

	def __init__(self, ip_address):

		(self.ip_address,
		 self.geoid,
		 self.locale_code,
		 self.continent_code,
		 self.continent_name,
		 self.country_iso_code,
	 	 self.country_name,
		 self.subdiv1_iso_code,
		 self.subdiv1_name,
		 self.subdiv2_iso_code,
		 self.subdiv2_name,
		 self.city_name,
		 self.metro_code,
		 self.time_zone) = [ip_address, None] + (["Unknown"]*12)

	def set_values(self, row):

		(self.geoid,
		 self.locale_code,
		 self.continent_code,
		 self.continent_name,
		 self.country_iso_code,
	 	 self.country_name,
		 self.subdiv1_iso_code,
		 self.subdiv1_name,
		 self.subdiv2_iso_code,
		 self.subdiv2_name,
		 self.city_name,
		 self.metro_code,
		 self.time_zone) = ["Unknown" if field == "" else field for field in row]

	# returns all geolocation data as a multi-line string
	def to_string(self):

		result  = "IP address: %s\n" % self.ip_address
		result += "Locale code: %s\n" % self.locale_code
		result += "Continent: %s (%s)\n" % (self.continent_name, self.continent_code)
		result += "Country: %s (%s)\n" % (self.country_name, self.country_iso_code)
		result += "Subdivision 1: %s (%s)\n" % (self.subdiv1_name, self.subdiv1_iso_code)
		result += "Subdivision 2: %s (%s)\n" % (self.subdiv2_name, self.subdiv2_iso_code)
		result += "City: %s\n" % self.city_name
		result += "Metro code: %s\n" % self.metro_code
		result += "Time zone: %s" % self.time_zone

		return result

	# returns all geolocation data as a JSON string
	def to_json(self):

		result = {
			"ip_address": self.ip_address,
			"locale_code": self.locale_code,
			"continent": {
				"name": self.continent_name,
				"code": self.continent_code
			},
			"country": {
				"name": self.country_name,
				"code": self.country_iso_code
			},
			"subdivision1": {
				"name": self.subdiv1_name,
				"code": self.subdiv1_iso_code
			},
			"subdivision2": {
				"name": self.subdiv2_name,
				"code": self.subdiv2_iso_code
			},
			"city": self.city_name,
			"metro_code": self.metro_code,
			"time_zone": self.time_zone
		}

		return json.dumps(result, indent=2)


def query_database(ip_address):

	"""
	Returns geolocation data for an IP address (represented as a string
	such as "1.2.3.4") as an IPInfo object.
	"""

	# convert the IP address into an integer and get its version
	try:
		(ip_integer,version) = ip_to_integer(ip_address)
	except:
		raise ValueError("invalid IP address")

	ip_info = IPInfo(ip_address)

	# obtain the name of the segment file in which the geoname ID for the
	# given IP address is stored
	geoid_segment = None
	try:
		index_filename = "database/index-geoid-ip%d" % version
		with open(index_filename, 'rb') as index_file:
			segment_num = 0
			while True:
				try:
					row = pickle.load(index_file)
					if row[0] <= ip_integer <= row[1]:
						geoid_segment = segment_num
						break
					segment_num += 1
				# if the IP address is not in any listed subnetwork
				except EOFError:
					return ip_info
	except:
		raise Exception("geoname ID index file was not found on database")

	# get the geoname ID for the given IP address
	geoid = None
	try:
		segment_filename = "database/geoid-ip%d-%d" % (version, geoid_segment)
		with open(segment_filename, 'rb') as segment_file:
			while True:
				try:
					row = pickle.load(segment_file)
					if row[0] <= ip_integer <= row[1]:
						geoid = row[2]
						break
				# if the IP address is not in any listed subnetwork
				except EOFError:
					return ip_info
	except IOError:
		raise Exception("geoname ID segment file was not found on database")

	# obtain the name of the segment file in which the geolocation data for
	# the given IP address is stored
	location_segment = None
	try:
		index_filename = "database/index-location"
		with open(index_filename, 'rb') as index_file:
			segment_num = 0
			# since we got a geoname ID, this loop MUST succeed
			while True:
				row = pickle.load(index_file)
				if row[0] <= geoid <= row[1]:
					location_segment = segment_num
					break
				segment_num += 1
	except:
		raise Exception("location index file was not found on database")

	# get the geolocation data for the given IP address
	try:
		segment_filename = "database/location-%d" % location_segment
		with open(segment_filename, 'rb') as segment_file:
			# since we got a geoname ID, this loop MUST succeed
			while True:
				row = pickle.load(segment_file)
				if row[0] == geoid:
					ip_info.set_values(row)
					break
	except:
		raise Exception("location segment file was not found on database")

	return ip_info

#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import json
import pickle

from config import *
from ipfunctions import *


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

	def to_string(self):

		result  = "IP address: %s\n" % self.ip_address
		result += "Continent: %s (%s)\n" % (self.continent_name, self.continent_code)
		result += "Country: %s (%s)\n" % (self.country_name, self.country_iso_code)
		result += "Subdivision 1: %s (%s)\n" % (self.subdiv1_name, self.subdiv1_iso_code)
		result += "Subdivision 2: %s (%s)\n" % (self.subdiv2_name, self.subdiv2_iso_code)
		result += "City: %s\n" % self.city_name
		result += "Metro code: %s\n" % self.metro_code
		result += "Time zone: %s" % self.time_zone

		return result

	def to_json(self):

		result = {
			"ip": self.ip_address,
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


##
# @brief returns all available information for a given IP address as an
#        IPInfo object
#
def query_database(ip_address):

	# convert the IP address into an integer ip_integer
	try:
		(ip_integer,version) = ip_to_integer(ip_address)
	except:
		raise ValueError("Invalid IP address.")

	ip_info = IPInfo(ip_address)

	# obtain the name of the file in which the geoname ID of the
	# given IP address is stored
	geoid_segment = None

	try:
		index_filename = "database/index-geoid-ip%d" % version
		with open(index_filename) as index_file:
			current = 0
			while True:
				try:
					row = pickle.load(index_file)
					if row[0] <= ip_integer <= row[1]:
						geoid_segment = current
						break
					current += 1
				except EOFError:
					return ip_info
	except:
		raise Exception("index file not found on database")

	# if the IP address is not in any subnetwork in the database
	if geoid_segment is None:
		return ip_info

	geoid = None

	# get the geoname ID for the given IP address
	try:
		geoid_filename = "database/geoid-ip%d-%d" % (version, geoid_segment)
		with open(geoid_filename) as segment_file:
			while True:
				try:
					row = pickle.load(segment_file)
					if row[0] <= ip_integer <= row[1]:
						geoid = row[2]
						break
				except EOFError:
					break
	except IOError:
		raise Exception("database does not exist or is corrupted")

	# obtain the name of the file in which the location of the given IP
	# address is stored
	location_segment = None

	try:
		index_filename = "database/index-location"
		with open(index_filename) as index_file:
			current = 0
			while True:
				row = pickle.load(index_file)
				if row[0] <= geoid <= row[1]:
					location_segment = current
					break
				current += 1
	except:
		raise Exception("database does not exist or is corrupted")

	# get the geographical information for the given IP address
	try:
		location_filename = "database/location-%d" % location_segment
		with open(location_filename) as segment_file:
			while True:
				row = pickle.load(segment_file)
				if row[0] == geoid:
					ip_info.set_values(row)
					break
	except:
		raise Exception("database does not exist or is corrupted")

	return ip_info

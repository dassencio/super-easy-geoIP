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

	# get the geoname ID for the given IP address
	if version == socket.AF_INET:
		block = ip4_block
		first = (ip_integer // block) * block
		last = first + block - 1
		filename = "database/geoid-ip4-%d-%d.bin" % (first, last)
	else:
		block = ip6_block
		first = (ip_integer // block) * block
		last = first + block - 1
		filename = "database/geoid-ip6-%d-%d.bin" % (first, last)

	if os.path.isfile(filename):
		with open(filename) as segment_file:
			while True:
				try:
					row = pickle.load(segment_file)
					if row[0] <= ip_integer <= row[1]:
						geoid = row[2]
						break
				except EOFError:
					break

	# get the available geographical information for the given IP address
	if geoid is not None:
		first = (geoid // geoid_block) * geoid_block
		filename = "database/city-%d-%d.bin" % (first, first+geoid_block-1)
		if os.path.isfile(filename):
			with open(filename) as segment_file:
				while True:
					try:
						row = pickle.load(segment_file)
						if row[0] == geoid:
							ip_info.set_values(row)
							break
					except EOFError:
						break

	return ip_info

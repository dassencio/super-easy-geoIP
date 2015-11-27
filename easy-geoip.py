#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import cgi
import argparse

from querydb import *


##
# @brief returns the queries sent to the server as a python dictionary
#
def get_queries():

	# queries sent to the server
	fs = cgi.FieldStorage()

	queries = {}
	for key in fs.keys():
		queries[key] = fs[key].value

	return queries


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--output-format', type=str, default="json",
	                    help='specify the output format (default: json)')
	parser.add_argument('-i', '--ip-address', type=str, default=None,
	                    help='IP address')
	namespace = parser.parse_args()

	output_format = namespace.output_format
	ip_address = namespace.ip_address

	# the Content-type header will only be shown if this script is
	# executed on a web server, i.e., it will not be displayed on
	# a terminal (unless you define an environment variable called
	# "REMOTE_ADDR")
	show_header = False

	# this part only applies if the script is executed on a web server
	if "REMOTE_ADDR" in os.environ.keys():
		show_header = True
		ip_address = os.environ["REMOTE_ADDR"]
		queries = get_queries()
		if 'q' in queries:
			ip_address = queries['q']
		if 'format' in queries:
			output_format = queries['format']

	if show_header:
		if output_format == "json":
			print("Content-type: application/json; charset= utf-8\n")
		else:
			print("Content-type: text/plain; charset= utf-8\n")

	try:
		ip_info = query_database(ip_address)
		if output_format == "json":
			print(ip_info.to_json())
		elif output_format == "plain":
			print(ip_info.to_string())
		else:
			raise Exception("invalid output format (%s).", output_format)
	except Exception as e:
		print(str(e))
		sys.exit(1)


#!/usr/bin/env python3

import os
import sys
import cgi
import argparse

from querydb import *

################################################################################

def get_queries():

	"""Returns the queries sent to the server as a python dictionary."""

	# queries sent to the server
	fs = cgi.FieldStorage()

	queries = {}
	for key in fs.keys():
		queries[key] = fs[key].value

	return queries

################################################################################

if __name__ == '__main__':

	# this part only applies if the script is executed on a web server
	if "REMOTE_ADDR" in os.environ.keys():

		show_header = True
		queries = get_queries()

		if 'q' in queries:
			ip_address = queries['q']
		else:
			ip_address = os.environ["REMOTE_ADDR"]

		if 'format' in queries:
			output_format = queries['format']
		else:
			output_format = "json"
	else:
		show_header = False

		parser = argparse.ArgumentParser()
		parser.add_argument('-f', '--output-format', type=str, default="json",
				    help='specify the output format (default: json)')
		parser.add_argument('-i', '--ip-address', type=str, required=True,
				    help='IP address')
		namespace = parser.parse_args()

		output_format = namespace.output_format
		ip_address = namespace.ip_address

	# the Content-type header will only be shown if this script is
	# executed on a web server, i.e., it will not be displayed on
	# a terminal (unless you define an environment variable called
	# "REMOTE_ADDR")
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
			raise Exception("invalid output format (%s)" % output_format)
	except Exception as e:
		if output_format == "json":
			import json
			print(json.dumps({"error": str(e)}, indent=2))
		else:
			print(str(e))
		sys.exit(1)


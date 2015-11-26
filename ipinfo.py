#!/usr/bin/python
# -*- coding: utf-8 -*-


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
	parser.add_argument('-n', '--no-header', action='count', default=False,
	                    help='omit Content-type header (default: no)')
	parser.add_argument('-i', '--ip-address', type=str, default=None,
	                    help='IP address')
	namespace = parser.parse_args()

	output_format = namespace.output_format
	show_header = not namespace.no_header
	ip_address = namespace.ip_address

	# first try the queries sent to the server
	queries = get_queries()
	if 'q' in queries:
		ip_address = queries['q']
	if 'format' in queries:
		output_format = queries['format']

	# if no IP address was sent via queries, take the user's IP
	if ip_address is None and "REMOTE_ADDR" in os.environ.keys():
		ip_address = os.environ["REMOTE_ADDR"]

	if show_header:
		if output_format == "json":
			print("Content-type: application/json; charset= utf-8\n")
		else:
			print("Content-type: text/plain; charset= utf-8\n")

	try:
		ip_info = query_database(ip_address)
	except Exception as e:
		print(str(e))
		sys.exit(1)

	if output_format == "json":
		print(ip_info.to_json())
	elif output_format == "plain":
		print(ip_info.to_string())
	else:
		print("Invalid output format.")
		sys.exit(1)


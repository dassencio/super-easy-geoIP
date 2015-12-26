#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import binascii


def netmask_to_ip_range(netmask_cidr):

	"""
	Returns a tuple (ip_lower, ip_upper) containing the integer
	representation of the lower and upper IP address values in the
	range specified by a given netmask string in CIDR notation.

	Both IPv4 netmasks (e.g. "192.168.1.1/24") and IPv6 netmasks
	(e.g. "2a02:a448:ddb0::/44") are accepted.
	"""

	try:
		fragments = netmask_cidr.split('/')
		ip_address = fragments[0]
		netmask_len = int(fragments[1])

		for (max_len, version) in ((32,socket.AF_INET), (128,socket.AF_INET6)):

			try:
				suffix_mask = (1 << (max_len - netmask_len)) - 1
				netmask = ((1 << max_len) - 1) - suffix_mask
				ip_hex = socket.inet_pton(version, ip_address)
				ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask

				return (ip_lower, ip_lower + suffix_mask)
			except:
				pass
	except:
		pass

	raise ValueError("invalid netmask")


def ip_to_integer(ip_address):

	"""
	Converts an IP address to its representation as an integer value
	and returns a tuple (ip_integer, version), with version being
	either 4 or 6.

	Both IPv4 addresses (e.g. "192.168.1.1") and IPv6 addresses
	(e.g. "2a02:a448:ddb0::") are accepted
	"""

	# try parsing the IP address first as IPv4, then IPv6
	for version in (socket.AF_INET, socket.AF_INET6):

		try:
			ip_hexstr = socket.inet_pton(version, ip_address)
			ip_integer = int(binascii.hexlify(ip_hexstr), 16)

			return (ip_integer, 4 if version == socket.AF_INET else 6)
		except:
			pass

	raise ValueError("invalid IP address")

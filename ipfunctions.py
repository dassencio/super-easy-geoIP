#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import binascii


def subnetwork_to_ip_range(subnetwork_cidr):

	"""
	Returns a tuple (ip_lower, ip_upper) containing the integer values
	of the lower and upper IP addresses respectively in a subnetwork
	expressed in CIDR notation (as a string).

	Both IPv4 subnetworks (e.g. "192.168.1.1/24") and IPv6 subnetworks
	(e.g. "2a02:a448:ddb0::/44") are accepted.
	"""

	try:
		fragments = subnetwork_cidr.split('/')
		network_prefix = fragments[0]
		netmask_len = int(fragments[1])

		# try parsing the subnetwork first as IPv4, then IPv6
		for version in (socket.AF_INET, socket.AF_INET6):

			ip_len = 32 if version == socket.AF_INET else 128

			try:
				suffix_mask = (1 << (ip_len - netmask_len)) - 1
				netmask = ((1 << ip_len) - 1) - suffix_mask
				ip_hex = socket.inet_pton(version, network_prefix)
				ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask
				ip_upper = ip_lower + suffix_mask

				return (ip_lower, ip_upper)
			except:
				pass
	except:
		pass

	raise ValueError("invalid subnetwork")


def ip_to_integer(ip_address):

	"""
	Converts an IP address expressed as a string to its representation
	as an integer value and returns a tuple (ip_integer, version), with
	version being either 4 or 6.

	Both IPv4 addresses (e.g. "192.168.1.1") and IPv6 addresses
	(e.g. "2a02:a448:ddb0::") are accepted.
	"""

	# try parsing the IP address first as IPv4, then IPv6
	for version in (socket.AF_INET, socket.AF_INET6):

		try:
			ip_hex = socket.inet_pton(version, ip_address)
			ip_integer = int(binascii.hexlify(ip_hex), 16)

			return (ip_integer, 4 if version == socket.AF_INET else 6)
		except:
			pass

	raise ValueError("invalid IP address")

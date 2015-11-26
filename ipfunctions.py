#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import binascii


##
# @brief returns a tuple (lower,upper) containing the integer representation
#        of the lower and upper bounds of the IP address range specified by
#        an input netmask
# @note the netmask may be either an IPv4 netmask (e.g. "192.168.1.1/24") or
#       an IPv6 netmask (e.g. "2a02:a448:ddb0::/44")
#
def netmask_to_ip_range(netmask_cidr):

	try:
		fragments = netmask_cidr.split('/')
		ip_address = fragments[0]
		netmask_len = int(fragments[1])

		for (max_len, version) in [(32,socket.AF_INET), (128,socket.AF_INET6)]:

			try:
				suffixmask = (1 << (max_len - netmask_len)) - 1
				netmask = ((1 << max_len) - 1) - suffixmask
				ip_hex = socket.inet_pton(version, ip_address)
				lower = int(binascii.hexlify(ip_hex), 16) & netmask

				return (lower, lower + suffixmask)
			except:
				pass
	except:
		pass

	raise ValueError("invalid netmask")


##
# @brief converts an IP address into an integer value
# @return (IP as integer, IP version)
# @note either IPv4 addresses (e.g. "192.168.1.1") or IPv6 addresses
#       (e.g. "2a02:a448:ddb0::") are accepted
#
def ip_to_integer(ip_address):

	# try parsing the input as IPv4, then IPv6
	for version in (socket.AF_INET, socket.AF_INET6):

		try:
			ip_hexstr = socket.inet_pton(version, ip_address)
			ip_integer = int(binascii.hexlify(ip_hexstr), 16)

			return (ip_integer, version)
		except:
			pass

	raise ValueError("invalid IP address")

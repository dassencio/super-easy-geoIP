Description
===========

easy-geoIP is an easy-to-install and easy-to-use IP geolocation engine. It
can work either as server or as a stand-alone command-line tool. If you want
to get an IP geolocation server in a matter of seconds, you are at the right
place!


Installation Instructions
=========================

Installing easy-geoIP is super easy. You can either do the steps below
locally on your machine and or directly on the server on which easy-geoIP
will be hosted. If you choose the first option, you can then copy the files
to the server later via FTP.

Besides closing this repository, the only thing you need to do is generate the
IP geolocation database. Just open a terminal and run:

	./generatedb

This script will automatically download, extract and segment the GeoLite2
database from MaxMind (available at http://dev.maxmind.com/geoip/geoip2/geolite2/).
Running this script again will remove the currently existing database and
regenerate it; I recommend you do this at least once every month (or every few
months) to make sure the geolocation data is accurate.

If you (or your web host provider) use Apache, the server should already be
working. Try opening the root page where you are hosting easy-geoIP
(e.g. ``my-domain.org/geoip``); if everything is working, you will see the
geolocation data for you own IP address. This is the type of output you should
see:

	{
	  "subdivision1": {
	    "code": "CA",
	    "name": "California"
	  },
	  "city": "Mountain View",
	  "time_zone": "America/Los_Angeles",
	  "subdivision2": {
	    "code": "Unknown",
	    "name": "Unknown"
	  },
	  "country": {
	    "code": "US",
	    "name": "United States"
	  },
	  "ip": "8.8.8.8",
	  "continent": {
	    "code": "NA",
	    "name": "North America"
	  },
	  "metro_code": "807"
	}

To select an IP address other than yours, just specify it directly on the
URL using a query string in the format ``my-domain.org/geoip?q=<IP>``. For
instance, to get the geolocation data for IP ``1.2.3.4``, open this URL:

	http://mydomain.org/?q=1.2.3.4&format=plain

By default, easy-geoIP yields JSON output. If you wish to get output in
plain text format, specify it directly on the URL as in the example below:

	http://mydomain.org/?q=1.2.3.4&format=plain


Using easy-geoIP as a stand-alone command-line tool
==================================================

You don't need to use easy-geoIP as a server. After you generate the database,
you can get IP geolocation data directly on your terminal. For that, just run
``ipinfo.py`` directly. Here is an example:

	./ipinfo.py -i 8.8.8.8

You can specify the output format too. For instance, to output plain text
instead of JSON, run:

	./ipinfo.py -f plain -i 8.8.8.8


License
=======

All code from this project is licensed under the GPLv3. See 'LICENSE' for more.


Contributors & Contact Information
==================================

Diego Assencio / diego@assencio.com


#
# Sizes of IPv4/6 netmask blocks. Decreasing these numbers will increase the
# querying speed but will also increase the number of files in the database
# (which in turn will slow down the database generation).
#
ip4_block = 1000
ip6_block = 1000

#
# Size of geoname ID blocks. Increasing this number will increase the querying
# speed but will also increase the number of files in the database (which in
# turn will slow down the database generation).
#
geoid_block = 500

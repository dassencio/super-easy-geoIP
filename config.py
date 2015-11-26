#
# Sizes of IPv4/6 address blocks. Decreasing these numbers will increase the
# querying speed but will also increase the number of files in the database
# (which in turn will slow down the database generation).
#
ip4_block = 1 << 23
ip6_block = 1 << 118

#
# Size of a geoname ID block. Increasing this number will increase the querying
# speed but will also increase the number of files in the database (which in
# turn will slow down the database generation).
#
geoid_block = 1 << 14

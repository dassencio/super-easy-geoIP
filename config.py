################################################################################
#
#  IMPORTANT: if you change the numbers below, regenerate the database
#             otherwise the querying script will stop working properly!
#
################################################################################

#
# Sizes of IPv4/6 netmask blocks. Increasing these numbers will increase the
# speed of the querying database (netmask -> geoname ID) segment files (since
# there will be more of them and they will be therefore smaller) at the cost of
# decreasing the speed of querying the associated index file (since it will be
# bigger: more segments => longer index).
#
ip4_block = 1000
ip6_block = 1000

#
# Size of geoname ID blocks. Increasing this number will increase the speed of
# querying the database (geoname ID -> geographical information) segment files
# (since there will be more of them and they will be therefore smaller) at the
# cost of decreasing the speed of querying the associated index file (since it
# will be bigger: more segments => longer index).
#
geoid_block = 500

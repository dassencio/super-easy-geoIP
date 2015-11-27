################################################################################
#
#  IMPORTANT: regenerate the database if you change the numbers below,
#             otherwise the querying script will stop working properly!
#
################################################################################

#
# Sizes of IPv4/6 netmask blocks. Decreasing these numbers will increase the
# querying speed for database (netmask -> geoname ID) segment files (since
# there will be more of them and they will be therefore smaller) at the cost of
# decreasing the querying speed for the associated index file (since it will be
# bigger: more segments => longer index).
#
ip4_block = 1000
ip6_block = 1000

#
# Size of geoname ID blocks. Decreasing this number will increase the querying
# speed for the database (geoname ID -> geolocation data) segment files (since
# there will be more of them and they will be therefore smaller) at the cost
# of decreasing the querying speed for the associated index file (since it
# will be bigger: more segments => longer index).
#
geoid_block = 500

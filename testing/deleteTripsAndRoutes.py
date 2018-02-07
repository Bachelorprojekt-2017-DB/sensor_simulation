#!/usr/bin/python2.5

#This script can be used to create GTFS files for testing purposes.
#The third parameter is a list of routes that will be kept from the original feed.
#The list is entered like this: "[0,1,2]"
#Use fix_stop_times.sh after using this script and at last use "filter_unused_stops.py" from the google transitfeed github page.

import sys
import transitfeed
import optparse

def main():
	parser = optparse.OptionParser(usage="usage: %prog [options] input_feed output_feed", version="%prog "+transitfeed.__version__)
	(options, args) = parser.parse_args()
	
	input_feed = args[0]
	output_feed = args[1]
	routes_to_keep = args[2].strip('[]').split(',')

	loader = transitfeed.Loader(input_feed)
	schedule = loader.Load()

	print "Removing trips where route_id is not " + str(routes_to_keep)
	for trip_id, trip in schedule.trips.items():
		if not trip.route_id in routes_to_keep:
			trip.ClearStopTimes()
			del schedule.trips[trip.trip_id]
  
	print "Removing routes where route_id is not " + str(routes_to_keep)
	for route_id, route in schedule.routes.items():
		if not route.route_id in routes_to_keep:
			del schedule.routes[route.route_id]
		
	schedule.WriteGoogleTransitFeed(output_feed)

if __name__ == "__main__":
	main()
import os
import pygtfs

DB_NAME = "db_fernstrecke"

database_location = os.path.join(os.path.dirname(__file__),
                                     DB_NAME)
data_location = os.path.join(os.path.dirname(__file__),
                                     "../data")

if(os.path.isfile(database_location)):
    schedule = pygtfs.Schedule(database_location)
    print("Database detected at", database_location,"\n")
else:
    schedule = pygtfs.Schedule(database_location)
    pygtfs.append_feed(schedule, data_location)
    print("Created new database at", database_location,"\n")

example_route = schedule.routes[5]
example_trip = example_route.trips[0]
stops = schedule.stops_by_id
stop1 = example_trip.stop_times[1]
stop2 = example_trip.stop_times[2]

print(example_route.route_long_name, "\n")
print(example_trip.stop_times[1].stop_sequence)
print("Halt 1: ")
print(stops(stop1.stop_id), "\n")
print(stop1.arrival_time, "\n")
print(stop1.departure_time, "\n")
print("Halt 2: ")
print(stops(stop2.stop_id), "\n")
print(stop2.arrival_time, "\n")
print(stop2.departure_time, "\n")

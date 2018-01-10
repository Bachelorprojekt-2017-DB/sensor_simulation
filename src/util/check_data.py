from datetime import date
import os
import pygtfs

def create_schedule():
	database_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'database')
	if os.path.isfile(database_path):
		schedule = pygtfs.Schedule(database_path)
	else:
		schedule = pygtfs.Schedule(database_path)
		pygtfs.append_feed(schedule, path)
	return schedule

def min_max_date(schedule):
	min_date = date.max
	max_date = date.min
	for service_exception in schedule.service_exceptions:
		cur_date = service_exception.date
		if cur_date < min_date:
			min_date = cur_date
		elif cur_date > max_date:
			max_date = cur_date
	print('Min date: {}, max date: {}'.format(min_date, max_date))

def get_highest_id(schedule):
	highest = 0
	for service_exception in schedule.service_exceptions:
		if highest < int(service_exception.id):
			highest = int(service_exception.id)
	return highest

def highest_route_count(schedule):
	highest_id = get_highest_id(schedule)
	route_counts = [0] * (highest_id + 1)
	for service_exception in schedule.service_exceptions:
		route_counts[int(service_exception.id)] += 1
	for route_count in route_counts:
		if route_count > 360:
			print(route_count)

def main():
	schedule = create_schedule()
	min_max_date(schedule)
	highest_route_count(schedule)

if __name__ == '__main__':
	main()
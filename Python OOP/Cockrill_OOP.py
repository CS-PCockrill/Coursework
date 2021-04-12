#-------------------------------------------------------------------------------
# Name: Patrick Cockrill
# Project 6
# Due Date: May 5th, 2019
#-------------------------------------------------------------------------------

import math

class Bus:
	def __init__(self, name, max_people, speed_fps):
		self.name = str(name)
		if max_people < 0:
			print("Max people cant be negative")
		else:
			self.max_people = int(max_people)
		if speed_fps < 0:
			print("Speed fps cant be negative")
		else:
			self.speed_fps = int(speed_fps)
		self.num_people = 0

	#this method overrides the base implementation of str ()
	def __str__(self):
		mph = format((self.speed_fps / 1)*(1/5280)*(60)*(60), '.2f') #Feet to miles
		return 'Bus named {} with {} people will travel at {}mph'.\
		format(self.name, self.num_people, mph)

	def time_to_travel(self, distance_feet):
		return int(distance_feet / self.speed_fps)

	def load_people(self, num_people):
		onboarding = num_people + self.num_people
		if onboarding <= self.max_people:
			self.num_people += num_people
			return True
		else:
			return False

	def unload_people(self, num_people):
		unloading = self.num_people - num_people
		if unloading >= 0:
			self.num_people -= num_people
			return True
		else:
			return False


class Town:
	def __init__(self, name, loc_x, loc_y, stop_time):
		self.name = name
		self.loc_x = loc_x
		self.loc_y = loc_y
		self.stop_time = stop_time

	def __str__(self):
		stopTime = format(round(self.stop_time / 60,2), '.2f')
		return '{} ({},{}). Exchange time: {} minutes'.\
		format(self.name, self.loc_x, self.loc_y, stopTime)

	#this method overrides the base implementation of the comparison.
	def __eq__(self, other):
		if self.loc_x == other.loc_x and self.loc_y == other.loc_y:
			return True
		else:
			return False


	def distance_to_town(self, town):
		#the formula of the distance between points in the Cartesian plane is used
		distanceTill = math.sqrt(((town.loc_x - self.loc_x)**2) + ((town.loc_y - self.loc_y)**2))
		return distanceTill


class Journey(Bus, Town):

	def __init__(self, bus, destinations=None, start_time=0):
		self.bus = bus
		if destinations != None:
			self.destinations = destinations
		else:
			self.destinations = []
		self.start_time = start_time

	# this method overrides the base implementation of str ()
	def __str__(self):
		Journey = 'Journey with {} stops:\n'.format(len(self.destinations))
		for i in self.destinations:
			Journey += '\t{}\n'.format(i)
		return Journey + 'Bus Information: {}\n'.format(str(self.bus)) #more reuse - less code

	def add_destination(self, town):
		self.destinations.append(town)
		return None

	def town_in_journey(self, town):
		if town in self.destinations:
			return True
		else:
			return False

	def check_journey_includes(self, start_town, dest_town):
		if self.town_in_journey(start_town) and self.town_in_journey(start_town): #more reuse - less code
			start_index = self.destinations.index(start_town)
			if dest_town in self.destinations[start_index:]:
			#uses a sublist, we need a segment starts with index
				return True
			else:
				return False
		else:
			return False

	def total_journey_distance(self):
		total_distance = 0.0
		for town in self.destinations[:-1]:
			# index() returns index of the first occurrence in the list.
			total_distance += town.distance_to_town(self.destinations[self.destinations.index(town)+1])
		return  total_distance

	def town_arrival_time(self, town):
		#if the city is not in the route - return None
		if not self.town_in_journey(town):
			return None
		time = self.start_time
		for town_of_journey in self.destinations:
			# For the towns in the destinations...
			if town_of_journey == town:
				break
			time += town_of_journey.stop_time
			# index() returns index of the first occurrence in the list.
			time += town_of_journey.distance_to_town(self.destinations[self.destinations.index(town_of_journey)+1])/\
					self.bus.speed_fps

		return int(time)

	def town_departure_time(self, town):
		# if the city is not in the route - returns None
		if not self.town_in_journey(town):
			return None
		time = self.start_time
		#if the town is visited more than once on the journey, the last time the bus leaves the town should be returned
		town_repeated = self.destinations.count(town)
		#specify how many times a particular town is occure in the list
		town_occurences_marked = 0
		# for towns in the list of destinations...
		for town_of_journey in self.destinations:
			if town_of_journey == town:
				town_occurences_marked += 1
				#If the index == occurences of the town in the route, then it's the last visit
				if town_occurences_marked == town_repeated:
					time += town_of_journey.stop_time
					break
			time += town_of_journey.stop_time
			time += town_of_journey.distance_to_town(
				self.destinations[self.destinations.index(town_of_journey) + 1]) / self.bus.speed_fps
		return int(time)


	def total_journey_time(self):
		# returns the total time between departure and start
		return self.town_departure_time(self.destinations[-1]) - self.start_time
		#more reuse - less code

	def all_people_accommodated(self, unload_list, load_list):
		#iterating by indices. Since the three lists have the same length
		for index in range(0, len(unload_list)):
			if self.bus.unload_people(unload_list[index]):
				if self.bus.load_people(load_list[index]):
					continue
				else:
					return False
			else:
				return False
		return True

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# grew up on MC Escher drive, had to walk
# up hill bothways

import os
import sys
import copy
import json
import time
import collections


class MazeSolver:
	def __init__(self, maze):
		self._maze = maze

		# dictionary of locations storing previous location
		# and total distance from start
		self._locations = collections.defaultdict(
			lambda: {
				"distance": None, 
				"previous": None,
				"iteration": None
			}
		)

		# queue of locations to evaluate
		self._loc_queue = []

		# list of all locations that have been evaluated
		self._finished_locations = []

		self._solution = None

		# the maze is always a square so store the length
		# of one side for easy access
		self._maze_side = len(maze)
		
		# store the start and end location
		self._start = (0, 0)
		self._end = (self._maze_side-1, self._maze_side-1)

		self._loc_queue = [self._start]

		self._locations[self._start]["distance"] = 0

	def solve(self):

		i = 0
		while self._loc_queue:
			# pop the next location from cur_locations
			cur_location = self._loc_queue.pop(0)

			# new distance is one spot further than current location
			new_dist = self._locations[cur_location]["distance"] + 1

			if cur_location == self._end:
				self._compile_solution()
				
				self._locations[self._end]["iteration"] = i
				
				self._finished_locations.append(cur_location)

				print("Final Solution:")
				break

			# get all valid neighbors of current location
			neighbors = self._get_neighbors(cur_location)

			# print("current location {}".format(cur_location))
			# print("neighbors {}".format(neighbors))
			# print("")

			# check if any neighbors haven't been visited yet or
			# have a distance greater than new_dist, update their
			# info
			for n in neighbors:
				# skip any positions with a shorter distance 
				if (
					self._locations[n]["distance"] is not None
					and new_dist < self._locations[n]["distance"]
				):
					continue

				self._locations[n]["distance"] = new_dist
				self._locations[n]["previous"] = cur_location

				self._loc_queue.append(n)

				# print("{}: {}".format(n, self._locations[n]))


			# sort the positions in the queue by current distance
			# plus the distance to the exit
			self._loc_queue = sorted(
				self._loc_queue, 
				key=lambda x: (
					self._locations[x]["distance"] + 
					(2 * self._maze_side - (x[0] + x[1]))
				)
			)

			# print("queue {}".format(self._loc_queue))
			
			self._finished_locations.append(cur_location)

			self._locations[cur_location]["iteration"] = i

			self._print_debug()
			print("")
			time.sleep(0.1)

			i += 1
			if i > 10000:
				# print("breaking!")
				break

		else:
			print("No solution found!")

		self._print_debug()

	def _print_debug(self):
		print("+" + "-"*(self._maze_side*5) + "+")
		for y, col in enumerate(self._maze):
			row_str = "|"
			for x, wall in enumerate(col):
				if wall:
					row_str += "#####"
				else:
					d = self._locations[(x,y)]["distance"]
					# d = self._locations[(x,y)]["iteration"]
					if d is None or (
						self._solution and (x,y) not in self._solution
					):
						row_str += "     "
					else:
						row_str += "{:^5}".format(d)
			row_str += "|"
			print(row_str)
		print("+" + "-"*(self._maze_side*5) + "+\n")


	def _get_neighbors(self, position):
		x, y = position

		neighbors = [
			(x-1, y),
			(x+1, y),
			(x, y-1),
			(x, y+1)
		]

		neighbors = [
			n for n in neighbors
			if (
				n[0] >= 0 and n[0] < self._maze_side
				and n[1] >= 0 and n[1] < self._maze_side
				and self._maze[n[1]][n[0]] == 0
				and n not in self._finished_locations
			)
		]

		return neighbors

	def _compile_solution(self):
		self._solution = []
		cur_location = self._end
		while cur_location is not None:
			self._solution.append(cur_location)
			cur_location = self._locations[cur_location]["previous"]


def parse_file():
	if len(sys.argv) != 2:
		print("Please enter a single file path.")
		return
	
	test_file = os.path.abspath(sys.argv[1])

	if not os.path.isfile(test_file):
		print("Please enter path to json test file.")
		return

	# TODO ensure file is json

	with open(test_file, "r") as f:
		maze_layout = json.load(f)

	# TODO ensure maze layout is 2D list with 1s and 0s 

	return maze_layout


if __name__ == "__main__":
	maze_layout = parse_file()

	maze_solver = MazeSolver(maze_layout)

	maze_solver.solve()

	#maze_solver.print_solution()

import sys
import json
import time
import random


class MazeGenerator:
	def __init__(self, side, use_last=True, animate=False):

		self._side = side
		self._total_count = 2*side - 1

		self._use_last = use_last

		self._animate = animate

		# generate starting maze with all
		# spaces blocked by walls
		self._maze = [
			[0] * self._total_count
			for i in range(self._total_count)
		]

		# initialize the currently visited spots to
		# the starting top-left corner
		self._current_spots = [(0,0)]
		self._maze[0][0] = 1

		# add the remaining spots to the list of
		# not-yet-been-visited spots
		self._new_spots = [
			(i, j) 
			for i in range(self._side) 
			for j in range(self._side)
		][1:]

	def generate_maze(self):
		if self._animate:
			self.print_maze()

		while self._current_spots:

			# self.print_debug()
			
			# use the last spot in the stack
			if self._use_last:
				cur_spot = self._current_spots[-1]

			# pick a random spot in the stack
			else:
				cur_spot = self._current_spots[
					random.randint(0, len(self._current_spots)-1)
				]

			# get remaining valid neighbors of current spot
			neighbors = self._find_neighbors(cur_spot)

			# if no more valid neighbors, then the current
			# spot is done so remove it from the stack
			if not neighbors:
				self._current_spots.remove(cur_spot)
				continue

			# connect the current spot to a random neighbor
			self._connect_cur_spot(cur_spot, neighbors)

			if self._animate:
				self.print_maze()
				time.sleep(0.1)

	def _find_neighbors(self, spot):
		neighbors = [
			(spot[0]-1, spot[1]),
			(spot[0]+1, spot[1]),
			(spot[0], spot[1]-1),
			(spot[0], spot[1]+1),
		]

		neighbors = [
			n for n in neighbors
			if (
				n[0] >= 0 and n[0] < self._side and
				n[1] >= 0 and n[1] < self._side and
				n in self._new_spots
			)
		]

		return neighbors

	def _connect_cur_spot(self, cur_spot, neighbors):
		
		# pick one at random
		# TODO add horizontal bias
		next_spot = neighbors[
			random.randint(0, len(neighbors)-1)
		]

		# make connection between both spots
		# change maze location to 1
		wall = (
			int((cur_spot[0]*2 + next_spot[0]*2) * 0.5),
			int((cur_spot[1]*2 + next_spot[1]*2) * 0.5)
		)

		# print("Wall {}".format(wall))

		self._maze[next_spot[0]*2][next_spot[1]*2] = 1
		self._maze[wall[0]][wall[1]] = 1

		self._new_spots.remove(next_spot)

		self._current_spots.append(next_spot)

	def print_maze(self):
		print("+" + "-"*(self._total_count*2-1) + "+")
		for row in self._maze:
			row_str = "|"
			row_str += " ".join([" " if i else "#" for i in row])
			row_str += "|"
			print(row_str)
		print("+" + "-"*(self._total_count*2-1) + "+\n")

	def print_final_maze(self):
		print("[")
		maze_str = []
		for j in self._maze:
			maze_str.append("  {}".format([
				int(not bool(i)) for i in j
			]))
		print(",\n".join(maze_str))
		print("]")

	def print_debug(self):
		print("New spots:\n{}\n".format(json.dumps(self._new_spots)))
		print("Current spots:\n{}\n".format(json.dumps(self._current_spots)))



if __name__ == "__main__":
	side = 15
	use_last_spot = True
	animate = False

	if len(sys.argv) > 1:
		side = int(sys.argv[1])
		if len(sys.argv) > 2:
			use_last_spot = sys.argv[2] == "True"
			if len(sys.argv) > 3:
				animate = sys.argv[3] == "True"

	maze_gen = MazeGenerator(side, use_last_spot, animate)

	maze_gen.generate_maze()

	maze_gen.print_final_maze()

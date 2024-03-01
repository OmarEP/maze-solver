from cell import Cell
import time
import random
class Maze(object):
	def __init__(
			self,
			x1, 
			y1,
			num_rows,
			num_cols,
			cell_size_x,
			cell_size_y,
			win=None,
			seed=None,
	):
			self._cells = []
			self._x1 = x1 
			self._y1 = y1 
			self._num_rows = num_rows
			self._num_cols = num_cols
			self._cell_size_x = cell_size_x
			self._cell_size_y = cell_size_y
			self._win = win 
			if seed:
				random.seed(seed)
			self._create_cells()
			self._break_entrance_and_exit()
			self._break_walls_r(0, 0)
			self._reset_cells_visited()


	def _create_cells(self):
		for i in range(self._num_cols):
			col_cells = []
			for j in range(self._num_rows):
				col_cells.append(Cell(self._win))
			self._cells.append(col_cells)
			
		for i in range(self._num_cols):
			for j in range(self._num_rows):
					self._draw_cell(i, j)
			
	def _draw_cell(self, i, j):
			if self._win is None:
				return
			
			x1 = self._x1 + i * self._cell_size_x
			y1 = self._y1 + j * self._cell_size_y
			x2 = x1 + self._cell_size_x
			y2 = y1 + self._cell_size_y
			self._cells[i][j].draw(x1, y1, x2, y2)
			self._animate()

	def _animate(self):
			if self._win is None:
				return
			self._win.redraw()
			time.sleep(0.05)

	def _break_walls_r(self, i, j):
		self._cells[i][j].visited = True 
		while True:
			coordinates = []
			if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
					coordinates.append((i + 1,j))
			if i - 1 >= 0 and not self._cells[i - 1][j].visited:
					coordinates.append((i - 1,j))
			if j - 1 >= 0 and not self._cells[i][j - 1].visited:
					coordinates.append((i, j - 1))
			if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
					coordinates.append((i, j + 1))
			if len(coordinates) == 0:
				self._draw_cell(i, j)
				return 
			direction = random.randrange(len(coordinates))
			chosen_direction = coordinates[direction]
			if chosen_direction[0] == i - 1:
				self._cells[i - 1][j].has_right_wall = False 
				self._cells[i][j].has_left_wall = False
			if chosen_direction[0] == i + 1:
				self._cells[i + 1][j].has_left_wall = False 
				self._cells[i][j].has_right_wall = False
			if chosen_direction[1] == j - 1:
				self._cells[i][j - 1].has_bottom_wall = False 
				self._cells[i][j].has_top_wall = False
			if chosen_direction[1] == j + 1:
				self._cells[i][j + 1].has_top_wall = False 
				self._cells[i][j].has_bottom_wall = False
			self._break_walls_r(chosen_direction[0], chosen_direction[1])

	def _reset_cells_visited(self):
		for col in self._cells:
			for cell in col:
				cell.visited = False

			
	def _break_entrance_and_exit(self):
			self._cells[0][0].has_top_wall = False 
			self._draw_cell(0, 0)
			self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
			self._draw_cell(self._num_cols - 1, self._num_rows - 1)
				

	
	def _solve_r(self, i=0, j=0):
		self._animate()
		self._cells[i][j].visited = True
		if self._cells[i][j] == self._cells[self._num_cols - 1][self._num_rows - 1]:
			return True 
		
		coordinates = []
		if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
				coordinates.append((i + 1,j))
		if i - 1 >= 0 and not self._cells[i - 1][j].visited:
				coordinates.append((i - 1,j))
		if j - 1 >= 0 and not self._cells[i][j - 1].visited:
				coordinates.append((i, j - 1))
		if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
				coordinates.append((i, j + 1))
		for coordinate in coordinates:
			if coordinate[0] == i - 1 and self._cells[i - 1][j].has_right_wall == False and self._cells[i][j].has_left_wall == False:
				self._cells[i][j].draw_move(self._cells[i-1][j])
				found = self._solve_r(i-1, j)
				if found:
					return True
				self._cells[i][j].draw_move(self._cells[i-1][j], True)

			if coordinate[0] == i + 1 and self._cells[i + 1][j].has_left_wall == False and self._cells[i][j].has_right_wall == False:
				self._cells[i][j].draw_move(self._cells[i+1][j])
				found = self._solve_r(i+1, j)
				if found:
					return True
				self._cells[i][j].draw_move(self._cells[i+1][j], True)

			if coordinate[1] == j - 1 and self._cells[i][j - 1].has_bottom_wall == False and self._cells[i][j].has_top_wall == False:
				self._cells[i][j].draw_move(self._cells[i][j-1])
				found = self._solve_r(i, j - 1)
				if found:
					return True
				self._cells[i][j].draw_move(self._cells[i][j-1], True)

			if coordinate[1] == j + 1 and self._cells[i][j + 1].has_top_wall == False and self._cells[i][j].has_bottom_wall == False:
				self._cells[i][j].draw_move(self._cells[i][j+1])
				found = self._solve_r(i, j + 1)
				if found:
					return True
				self._cells[i][j].draw_move(self._cells[i][j+1], True)

		return False
	
	def solve(self):
		return self._solve_r(0, 0)
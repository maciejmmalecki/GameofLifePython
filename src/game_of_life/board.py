import numpy as np

class Board:

    """This class represents the board in Conway's Game of Life.
    """

    def __init__(self, rows, cols):

        """
        Initialize the board

        :param rows: number of rows
        :param cols: number od columns

        """
        if rows <= 0 or cols <= 0:
            raise ValueError("Number of rows and columns should be positive.")
        self.cols = cols
        self.rows = rows
        self.step_count = 0
        self.matrix = np.zeros((rows,cols), dtype = int)
        
    def clear(self):
        """This method clears the board"""

        self.step_count = 0
        self.matrix.fill(0)

    def empty(self) -> bool:
        """This method checks whether the board has no alive cells.

        Returns:
            bool:  It is True whether the cells: 0. Otherwise it it False 
        """
        return np.all(self.matrix == 0)

    def copy(self):
        """Creates a copy of the board

        Returns:
            Board:new board a new board with copied grid and step count
        """
        new_board = Board(self.rows, self.cols)
        new_board.matrix = np.copy(self.matrix)
        new_board.step_count = self.step_count
        return new_board
    
    def set_cell_value(self, row, col, state):
        """Sets value of a cell

        Args:
            row (int): row index
            col (int): column index
            state (int): 0 if cell is dead or 1 if cell is alive

        Raises:
            ValueError: whether state is not 0 or 2
            IndexError: if cell is outside the board
        """
        if state not in (0, 1):
            raise ValueError("Cell values should be 0-1")
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            raise IndexError("Cell is outside the board")
        self.matrix[row, col] = state

    def get_cell_value(self, row, col):

        """Gets value of a cell

        Args:
            row (int): row index
            col (int): column index

        Raises:
            IndexError: if cell is outside the board
        Returns:
            int: value of the cell (0 or 1)
        """
        if not 0 <= row < self.rows or not 0 <= col < self.cols:
            raise IndexError("Cell is outside the board")
        return self.matrix[row, col]
    
    def load_board_from_file(self, file):
        """Loads the board from a file .txt

        Args:
            file (str): path

        Raises:
            ValueError: if file is empty
            ValueError: wrong number of columns in the file
            ValueError: wrong values in cells in the file
            ValueError: wrong number of rows in the file
           
        """

        with open(file, 'r') as file_name:
            lines = file_name.readlines()
        if not lines:
            raise ValueError("File is empty")
        lines_length = len(lines[0].strip())
        for line in lines:
            if len(line.strip()) != lines_length:
                raise ValueError("Wrong number of columns in the file")
            if any (symbol not in ('0', '1') for symbol in line.strip()):
                raise ValueError("Wrong values in cells in the file")
        
        file_rows = len(lines)
        if file_rows != self.rows:
            raise ValueError("Wrong number of rows in the file")
        self.cols = lines_length
        self.matrix = np.zeros((self.rows, self.cols), dtype = int)
        for number_of_row, line in enumerate(lines):
            for number_of_col, symbol in enumerate(line.strip()):
                if symbol == '1':
                    self.matrix[number_of_row, number_of_col] = 1
        self.step_count = 0
    
    def save_board_to_file(self, file):
        """Saves the current board to the file .txt

        Args:
            file (str): path
        """

        with open(file, 'w') as file_name:
            for row in range(self.rows):
                line = ''.join(str(self.matrix[row, col]) for col in range(self.cols))
                file_name.write(line + '\n')

    def random_board(self, density=0.2):
        """Responsible for filling the board with random values (0 or 1)

        Args:
            density (float): It is a probablility of alive cell
        Raises:
            ValueError: Wrong density
        """

        if not (0 <= density <= 1):
            raise ValueError("Percent of alive cells should be 0-1")
        self.matrix = np.random.choice([0, 1], size=(self.rows, self.cols), p=[1-density, density])
        self.step_count = 0

    def show_board(self):

        """Prints the board
        """
        print(f"Step: {self.step_count}")
        for row in range(self.rows):
            line = ''.join('*' if self.matrix[row, col] == 1 else ' ' for col in range(self.cols))
            print(line)
        print("\n" + "-" * self.cols + "\n")
        

    def count_alive(self, row, col):
        """Counts the alive neighbours

        Args:
            row (int): row index
            col (int): column index

        Raises:
            IndexError: if cell is outside the board
        Returns:
            int: number of alive neighbours
        """

        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            raise IndexError("Cell is outside the board")
        number = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (0 <= r < self.rows) and (0 <= c < self.cols):
                    if (r != row or c != col) and self.matrix[r, c] == 1:
                        number += 1
        return number

    def step(self):
        """One iteration of game of life
        """

        new_matrix = np.copy(self.matrix)
        for row in range(self.rows):
            for col in range(self.cols):
                alive = self.count_alive(row, col)
                if self.matrix[row, col] == 1:
                    if alive < 2 or alive > 3:
                        new_matrix[row, col] = 0
                else:
                    if alive == 3:
                        new_matrix[row, col] = 1
        self.matrix = new_matrix
        self.step_count += 1

    def __str__(self):
        """Returns a string version of the board"""

        board_str = f"Step: {self.step_count}\n"
        for row in range(self.rows):
            line = ''.join('*' if self.matrix[row, col] == 1 else ' ' for col in range(self.cols))
            board_str += line + '\n'
        return board_str
    
    def change_to_tuple(self) -> tuple:
        """Changes the matrix to a tuple

        Returns:
            tuple: tuple
        """

        return tuple(map(tuple, self.matrix))
    
    def next_board(self):
        """Returns the new board which represents the next step

        Returns:
            Board: new board
        """

        next_board = self.copy()
        next_board.step()
        return next_board
    
    def is_stable(self, previous_board) -> bool:
        """Responsible for checking if the board is the same as in a previous state 

        Args:
            previous_board (Board): board in a previous state

        Returns:
            bool: It is true when boards are the same
        """

        return np.array_equal(self.matrix, previous_board.matrix)
    
    @classmethod
    def from_tuple(cls, state):

        """Creates a board from a tuple

        Returns:
            Board: new board
        """

        rows = len(state)
        cols = len(state[0]) if rows > 0 else 0
        board = cls(rows, cols)
        board.matrix = np.array(state, dtype=int)
        return board
    
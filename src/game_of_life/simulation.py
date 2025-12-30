import numpy as np
from typing import Set, Tuple

class Simulation:

    def __init__(self, board, max_number_of_steps: int = 1000, stop_simulation: bool = True):
        """Initialize simulation

        Args:
            board (Board): board
            max_number_of_steps (int): maximum number of steps
            stop_simulation (bool): stop simulation when loop is detected

        Raises:
            ValueError: if max_number_of_steps is not a positive number
        """

        if max_number_of_steps <= 0:
            raise ValueError("Max number of steps should be a positive number")
        self.board = board
        self.stop_simulation = stop_simulation
        self.max_number_of_steps = max_number_of_steps
        self.loop = False
        self.where_is_loop= None
        self.previous_boards: Set[Tuple[Tuple[int,...],...]] = set()
        self.previous_boards.add(self.board.change_to_tuple())

    def is_loop(self):
        """Responsible for checking if there is a loop

        Returns:
            bool: it is True if there is a loop
        """

        return self.loop
    
    def simulation_step(self):

        """Performs one step, changes board, finds the loop

        Returns:
            bool: it is true if simulation continues
        """

        self.board.step()
        if self.board.step_count >= self.max_number_of_steps:
            return False
        current_board_state = self.board.change_to_tuple()
        if current_board_state in self.previous_boards:
            self.loop = True
            self.where_is_loop = self.board.step_count
            if self.stop_simulation:
                
                return False
                   
        self.previous_boards.add(current_board_state)
        if len(self.previous_boards) > 10000:
            self.previous_boards.clear()
            self.previous_boards.add(current_board_state)
        if self.board.empty():
            self.loop = True
            self.where_is_loop = self.board.step_count
            if self.stop_simulation:
                return False

        return True
    
    def start_simulation(self):
        """Runs the simulation
        """

        if self.board.empty():
            self.loop = True
            self.where_is_loop = self.board.step_count
            return{
                'loop': False,
                'step_count': self.board.step_count,
                'board': self.board,
                'where_is_loop': None,
                'why': 'empty'
            }
        while True:
            continue_simulation = self.simulation_step()
            if not continue_simulation:
                break
        if self.board.step_count >= self.max_number_of_steps:
            why = 'max_number_of_steps'
        elif self.loop:
            why = 'loop'
        else:
            why = 'unknown'
        return{
            'loop': self.loop,
            'step_count': self.board.step_count,
            'board': self.board,
            'where_is_loop': self.where_is_loop,
            'why': why
        }
    
    def reset_simulation(self):
        """Resets the simulation
        """

        self.previous_boards.clear()
        self.loop = False
        self.where_is_loop = None
        self.board.step_count = 0
        self.previous_boards.add(self.board.change_to_tuple())

    def copy_current_board(self):
        """Returns a copy of a board

        Returns:
            np.ndarray: copy of a board
        """
        return np.copy(self.board.matrix)

class Video:

    def __init__(self, simulation: Simulation):
        """Initializes the video

        Args:
            simulation (Simulation): simulation to record
        """
        self.simulation = simulation
        self.frames = [self.simulation.copy_current_board()]
    
    def record(self):
        """Records state after one step in the simulation

        Returns:
            bool: it is true if simulation continues
        """
        continue_simulation = self.simulation.simulation_step()
        self.frames.append(self.simulation.copy_current_board())
        return continue_simulation

    def video_run(self):
        """Records all frames

        Returns:
            dict: frames, loop, step_count, where_is_loop, board, why
        """
        while True:
            continue_simulation = self.record()
            if not continue_simulation:
                break
        if self.simulation.loop:
            why = 'loop'
        elif self.simulation.board.step_count >= self.simulation.max_number_of_steps:
            why = 'max_number_of_steps'
        else:
            why = 'unknown'
        return {
            'frames': self.frames,
            'loop': self.simulation.is_loop(),
            'step_count': self.simulation.board.step_count,
            'where_is_loop': self.simulation.where_is_loop,
            'board': self.simulation.board,
            'why': why
        }
        
    def get_number_of_frames(self):
        """Returnes the number of frames that were recorded

        Returns:
            int: number of frames
        """
        return len(self.frames)
        

    
    
import unittest
from pathlib import Path
import sys
import os
import numpy as np
sys.path.insert(0,str(Path(__file__).parent.parent))
from game_of_life.board import Board
from game_of_life.simulation import Simulation
from game_of_life.simulation import Video

class SimulationTest(unittest.TestCase):

    def setUp(self):
        self.board = Board(6,6)
        self.simulation = Simulation(self.board, max_number_of_steps=1000, stop_simulation=False)

    def test_initialization(self):
        s = Simulation(self.board, max_number_of_steps=25, stop_simulation=True)
        self.assertEqual(s.max_number_of_steps, 25)
        self.assertTrue(s.stop_simulation)
        self.assertEqual(s.board, self.board)
        self.assertIsNone(s.where_is_loop)
        self.assertFalse(s.loop)
    
    def test_initialization_parameters(self):
        
        s=Simulation(self.board)
        self.assertEqual(s.max_number_of_steps, 1000)
        self.assertTrue(s.stop_simulation)

    def test_invalid_max_number_of_steps(self):
        
        with self.assertRaises(ValueError):
            Simulation(self.board, max_number_of_steps=-3)
        with self.assertRaises(ValueError):
            Simulation(self.board, max_number_of_steps=0)
    
    def test_empty_board(self):
        self.board.clear()
        s = Simulation(self.board, max_number_of_steps=15, stop_simulation=True)
        result = s.start_simulation()
        self.assertFalse(result['loop'])
        self.assertEqual(result['step_count'], 0)
        self.assertEqual(result['where_is_loop'], None)
        self.assertEqual(result['why'], 'empty')

    def test_stable_board(self):

        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        self.board.set_cell_value(3,2,1)
        self.board.set_cell_value(3,3,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        result = s.start_simulation()
        self.assertEqual(s.where_is_loop, 1)
        self.assertTrue(s.loop)
        self.assertEqual(result['why'], 'loop') 

    def test_loop_detection(self):
        
        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)   
        self.board.set_cell_value(2,3,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        result = s.start_simulation()
        self.assertTrue(result['loop'])
        self.assertEqual(result['step_count'], 2)
        self.assertEqual(result['where_is_loop'], 2)
        self.assertLessEqual(s.where_is_loop, 3)

    def test_smoke(self):
        filename = "test_smoke.txt"
        try:
            with open(filename, 'w') as file:
                file.write("010\n111\n010\n")
            board = Board(3,3)
            board.load_board_from_file(filename)
            s = Simulation(board, max_number_of_steps=10, stop_simulation=True)
            result = s.start_simulation()
            self.assertIn('step_count', result)
            self.assertIn('loop', result)
            self.assertIn('why', result)
            self.assertGreater(result['step_count'], 0)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_max_number_of_steps(self):

        self.board = Board(5,5)
        self.board.set_cell_value(2, 2, 1)
        s = Simulation(self.board, max_number_of_steps=5, stop_simulation=False)
        result = s.start_simulation()
        self.assertTrue(s.loop)
        self.assertEqual(result['why'], 'max_number_of_steps')
        self.assertEqual(result['step_count'], 5)

    def test_stop_simulation(self):

        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        s = Simulation(self.board, max_number_of_steps=100, stop_simulation=False)
        result = s.start_simulation()
        self.assertTrue(result['loop'])
        self.assertEqual(result['why'], 'max_number_of_steps')
        self.assertEqual(result['step_count'], 100)

    def test_simulation_step(self):

        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        continue_simulation = s.simulation_step()
        self.assertTrue(continue_simulation)
        self.assertEqual(s.board.step_count, 1)
        continue_simulation = s.simulation_step()
        self.assertFalse(continue_simulation)
        self.assertEqual(s.board.step_count, 2)
        continue_simulation = s.simulation_step()
        self.assertFalse(continue_simulation)
        self.assertTrue(s.loop)

    def test_copy_current_board(self):

        self.board.set_cell_value(1,1,1)
        self.board.set_cell_value(1,2,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        copied = s.copy_current_board()
        self.assertTrue(np.array_equal(np.array(copied), self.board.matrix))

    def test_is_loop(self):

        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        self.assertFalse(s.is_loop())
        s.start_simulation()
        self.assertTrue(s.is_loop())
    
    def test_reset(self):

        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        s.start_simulation()
        self.assertTrue(s.loop)
        self.assertIsNotNone(s.where_is_loop)
        s.reset_simulation()
        self.assertFalse(s.loop)
        self.assertIsNone(s.where_is_loop)
        self.assertEqual(s.board.step_count, 0)
        self.assertEqual(len(s.previous_boards), 1)
    
    def test_results(self):

        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        s = Simulation(self.board, max_number_of_steps=10, stop_simulation=True)
        result = s.start_simulation()
        self.assertIn('loop', result)
        self.assertIn('step_count', result)
        self.assertIn('board', result)
        self.assertIn('where_is_loop', result)
        self.assertIn('why', result)

    def test_record(self):

        video = Video(self.simulation)
        self.assertEqual(len(video.frames), 1)
        self.assertTrue(np.array_equal(video.frames[0], self.simulation.board.matrix))
    
    def test_record_frame(self):

        video = Video(self.simulation)
        self.board.set_cell_value(1,1,1)
        self.board.set_cell_value(1,2,1)
        for x in range(3):
            continue_simulation = video.record()
            self.assertEqual(len(video.frames), x + 2)
            self.assertTrue(np.array_equal(video.frames[-1], self.simulation.board.matrix))
            if not continue_simulation:
                break
    
    def test_video_run(self):

        video = Video(self.simulation)
        self.board.set_cell_value(2,1,1)
        self.board.set_cell_value(2,2,1)
        self.board.set_cell_value(2,3,1)
        result = video.video_run()
        self.assertIn('frames', result)
        self.assertIn('loop', result)
        self.assertIn('step_count', result)
        self.assertIn('where_is_loop', result)
        self.assertIn('board', result)
        self.assertIn('why', result)
        self.assertGreaterEqual(len(result['frames']), 2)
        self.assertEqual(result['step_count'], self.simulation.board.step_count)

    def test_get_number_of_frames(self):

        video = Video(self.simulation)
        self.board.set_cell_value(1,1,1)
        self.board.set_cell_value(1,2,1)
        for x in range(5):
            video.record()
            self.assertEqual(video.get_number_of_frames(), x + 2)
    
    def test_copied_frames(self):

        video = Video(self.simulation)
        self.board.set_cell_value(1,1,1)
        video.record()
        first_copy = np.copy(video.frames[1])
        self.board.set_cell_value(2,2,1)
        video.record()
        self.assertTrue(np.array_equal(video.frames[1], first_copy))
        
    
    def test_empty_number_of_frames(self):

        video = Video(self.simulation)
        self.assertEqual(video.get_number_of_frames(), 1)
    
    def test_record_empty_board(self):

        self.board.clear()
        video = Video(self.simulation)
        continue_simulation = video.record()
        self.assertTrue(continue_simulation)
        
    def test_cell(self):

        board = Board(3, 3)
        board.set_cell_value(1, 1, 1)
        s = Simulation(board, max_number_of_steps=10, stop_simulation=True)
        result = s.start_simulation()
        self.assertEqual(result['step_count'], 1)
        self.assertTrue(result['board'].empty())
        self.assertTrue(result['loop'])
        self.assertEqual(result['why'], 'loop')

    def test_large_max_number_of_steps(self):

       board = Board(5, 5)
       board.set_cell_value(0, 1, 1)
       board.set_cell_value(1, 2, 1)
       board.set_cell_value(2, 0, 1)
       board.set_cell_value(2, 1, 1)
       board.set_cell_value(2, 2, 1)
       s = Simulation(board, max_number_of_steps=20, stop_simulation=True)
       result = s.start_simulation()
       self.assertTrue(result['step_count'] <= 10000)
       self.assertTrue(result['loop'] or result['step_count'] == 10000)
       self.assertIn(result['why'], ['loop', 'max_number_of_steps'])

    def test_pattern_loop(self):
        
        board = Board(15, 15) 

        pattern = [
            (4,6), (4,7), (4,8),
            (5,4), (5,9),
            (6,4), (6,9),
            (7,4), (7,9),
            (8,6), (8,7), (8,8)
        ]
        for r, c in pattern:
            board.set_cell_value(r, c, 1)
        s = Simulation(board, max_number_of_steps=20, stop_simulation=True)
        result = s.start_simulation()
        self.assertTrue(result['loop'])
        self.assertLessEqual(result['step_count'], 20)
        self.assertEqual(result['why'], 'loop')

   
if __name__ == '__main__':
    unittest.main()


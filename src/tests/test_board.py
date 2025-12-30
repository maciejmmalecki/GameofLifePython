import unittest
import numpy as np
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from game_of_life.board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board(5, 5)

    def test_board_initialization(self):

        self.assertEqual(self.board.rows, 5)
        self.assertEqual(self.board.cols, 5)
        self.assertTrue(np.all(self.board.matrix == 0))
        self.assertEqual(self.board.step_count, 0)

    def test_random_board(self):

        self.board.random_board(density=0.5)
        self.assertEqual(self.board.step_count, 0)
        self.assertTrue(np.any(self.board.matrix == 1))

    def test_clear(self):

        self.board.random_board()
        self.board.clear()
        self.assertTrue(np.all(self.board.matrix == 0))
        self.assertEqual(self.board.step_count, 0)

    def test_cell_value(self):

        self.board.set_cell_value(2, 3, 1)
        self.assertEqual(self.board.get_cell_value(2, 3), 1)
        with self.assertRaises(ValueError):
            self.board.set_cell_value(0, 0, 2)
        with self.assertRaises(IndexError):
            self.board.set_cell_value(10, 10, 1)

    def test_count_alive_neighbours(self):

        self.board.set_cell_value(1, 1, 1)
        self.board.set_cell_value(1, 2, 1)
        self.assertEqual(self.board.count_alive(1, 1), 1)
        self.assertEqual(self.board.count_alive(0, 0), 1)

    def test_copy(self):

        self.board.set_cell_value(0, 0, 1)
        next_board = self.board.copy()
        self.assertTrue(np.array_equal(next_board.matrix, self.board.matrix))
        self.assertEqual(next_board.step_count, self.board.step_count)

    def test_save_load_file(self):

        filename = "test_board.txt"
        self.board.set_cell_value(0, 0, 1)
        self.board.save_board_to_file(filename)
        loaded_board = Board(self.board.rows, self.board.cols)
        loaded_board.load_board_from_file(filename)
        self.assertTrue(np.array_equal(self.board.matrix, loaded_board.matrix))
        os.remove(filename)

    def test_step(self):

        self.board.set_cell_value(1, 0, 1)
        self.board.set_cell_value(1, 1, 1)
        self.board.set_cell_value(1, 2, 1)
        self.board.step()
        self.assertEqual(self.board.get_cell_value(0, 1), 1)
        self.assertEqual(self.board.get_cell_value(1, 1), 1)
        self.assertEqual(self.board.get_cell_value(2, 1), 1)
        self.assertEqual(self.board.step_count, 1)

    def test_is_stable(self):

        self.board.set_cell_value(1, 0, 1)
        self.board.set_cell_value(1, 1, 1)
        self.board.set_cell_value(1, 2, 1)
        original = self.board.copy()
        self.board.step()
        self.assertFalse(self.board.is_stable(original))
        self.board.step()
        self.assertTrue(self.board.is_stable(original))

    def test_is_empty(self):

        self.assertTrue(self.board.empty())
        self.board.set_cell_value(0, 0, 1)
        self.assertFalse(self.board.empty())

    def test_str(self):

        self.board.set_cell_value(0, 0, 1)
        board_str = str(self.board)
        self.assertIn("Step:", board_str)
        self.assertIn(" ", board_str)
        self.assertIn("*", board_str)

    def test_change_to_from_tuple(self):

        self.board.set_cell_value(0, 0, 1)
        tup = self.board.change_to_tuple()
        next_board = Board.from_tuple(tup)
        self.assertTrue(np.array_equal(self.board.matrix, next_board.matrix))
        self.assertEqual(self.board.rows, next_board.rows)
        self.assertEqual(self.board.cols, next_board.cols)

    def test_wrong_file_format(self):

        filename = "wrong_file.txt"
        with open(filename, 'w') as file:
            file.write("012\n000\n")
        board = Board(1, 1)
        with self.assertRaises(ValueError):
            board.load_board_from_file(filename)
        os.remove(filename)


if __name__ == "__main__":
    unittest.main()

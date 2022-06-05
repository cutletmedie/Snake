import unittest
import main


class TestCases(unittest.TestCase):
    # def setUP(self):
    #     levels = {"first_level": main.Level(10, main.Snake([[10, 5], [9, 5], [8, 5], [7, 5]]), []),
    #               "second_level": main.Level(25, main.Snake([[1, 3], [1, 2], [1, 1]]), [[3, 8], [14, 4]])}
    #     levels_list = list(levels.keys())
    #     level_default_name = levels_list[0]
    #     self.state = main.State(level_default_name)
    #     self.snake = main.Snake([[10, 5], [9, 5], [8, 5], [7, 5]])
    #     self.food = main.Food([10, 5])
    #     self.current_level_index = main.State.

    def test_get_coords(self):
        self.assertEqual(main.get_coords([[10, 5], [9, 5], [8, 5], [7, 5]]),
                         [[400, 200], [360, 200], [320, 200], [280, 200]])
        self.assertEqual(main.get_coords([[5, 7], [8, 9]]),
                         [[200, 280], [320, 360]])
        self.assertEqual(main.get_coords([]), [])

    # def test_check_food(self):
    #     check = main.Snake.check_food(self.snake, self.state)
    #     self.assertEqual(check, True)

    # def test_check_level_next(self):
    #     self.assertEqual(main.State.check_next_level(self.state), True)


if __name__ == '__main__':
    unittest.main()

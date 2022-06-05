import unittest
import main
import pygame
import copy


class TestCases(unittest.TestCase):
    # def setUP(self):
    #     levels = {"first_level": main.Level(10, main.Snake([[10, 5], [9, 5], [8, 5], [7, 5]]), []),
    #               "second_level": main.Level(25, main.Snake([[1, 3], [1, 2], [1, 1]]), [[3, 8], [14, 4]])}
    #     levels_list = list(levels.keys())
    #     level_default_name = levels_list[0]
    #     self.state = main.State(level_default_name)
    #     self.snake = main.Snake([[10, 5], [9, 5], [8, 5], [7, 5]])
    #     self.food = main.Food([10, 5])

    def test_get_coords(self):
        self.assertEqual(main.get_coords([[10, 5], [9, 5], [8, 5], [7, 5]]),
                         [[400, 200], [360, 200], [320, 200], [280, 200]])
        self.assertEqual(main.get_coords([[5, 7], [8, 9]]),
                         [[200, 280], [320, 360]])
        self.assertEqual(main.get_coords([]), [])

    def test_check_food(self):
        # голова змеи на еде
        state = main.State(main.levels_list[0])
        state.objects = [main.Food(state.snake.position, 'monster'), main.Food([11, 5])]
        expected_len = state.snake.len - 1
        check = state.snake.check_food(state)
        self.assertEqual(state.snake.len, expected_len)
        self.assertEqual(check, True)

        # голова змеи на пустом блоке, еда прямо перед ней
        check = state.snake.check_food(state)
        self.assertEqual(check, False)

        # еды вообще нет на карте
        state = main.State(main.levels_list[1])
        check = state.snake.check_food(state)
        self.assertEqual(check, False)

        state.objects = [main.Food(state.snake.position, "apple")]
        expected_len = state.snake.len
        check = state.snake.check_food(state)
        self.assertEqual(state.snake.len, expected_len)
        self.assertEqual(check, True)

    def test_check_eat_fruit(self):
        state = main.State(main.levels_list[0])
        apple, monster, turtle, bad_apple, star, heart = 'apple', 'monster', 'turtle', 'bad_apple', 'star', 'heart'
        food_type = [apple, monster, turtle, bad_apple, star, heart]
        for type in food_type:
            state.snake.speed = 10
            score_before = state.score
            len_before = state.snake.len
            state.health = 10
            health_before = state.health
            state.snake.eat_fruit(state, main.Food(state.snake.position, type))
            if type == monster:
                expected = 10 + state.snake.speed_default * 0.25
                self.assertEqual(state.snake.speed, expected)
            if type == turtle:
                expected = 10 - state.snake.speed_default * 0.25
                self.assertEqual(state.snake.speed, expected)
                state.snake.speed = 5
                state.snake.eat_fruit(state, main.Food(state.snake.position, type))
                self.assertEqual(state.snake.speed, 5)
            if type == apple:
                self.assertEqual(state.score, score_before + 1)
            if type == bad_apple:
                self.assertEqual(state.snake.len, len_before - 1)
            if type == star:
                self.assertEqual(state.score, score_before + 3)
            if type == heart:
                self.assertEqual(state.health, health_before)
                state.health = 4
                state.snake.eat_fruit(state, main.Food(state.snake.position, type))
                self.assertEqual(state.health, 5)

    def test_check_level_next(self):
        state = main.State(main.levels_list[0])
        self.assertTrue(state.check_next_level())

        state = main.State(main.levels_list[-1])
        self.assertEqual(state.check_next_level(), False)

    def test_reset_snake(self):
        state = main.State(main.levels_list[0])
        state.snake = copy.deepcopy(main.Snake([[1, 3], [1, 2], [1, 1]]))
        state.reset_snake()
        expected = main.Snake([[10, 5], [9, 5], [8, 5], [7, 5]])
        self.assertEqual(state.snake.coords, expected.coords)

    def test_remove_food(self):
        objects = [main.Food([1, 1])]
        objects[0].remove_food(objects)
        self.assertEqual(objects, [])

    def check_generate_objects(self):
        state = main.State(main.levels_list[0])
        game = main.Game()
        game.generate_objects(state, game.surface)
        self.assertEqual(len(state.objects), 3)
        state.objects += [main.Food([1, 1])]
        self.assertEqual(len(state.objects), 4)


if __name__ == '__main__':
    unittest.main()

import copy
import pygame.locals
import random

pygame.display.set_caption('Snake by Monika Veltman')
PLAY, PICK_LEVEL, MAIN_MENU, QUIT, CONTINUE, NEXT_LEVEL, TRY_AGAIN = \
    "Играть", "Выбрать уровень", "Выйти в главное меню", "Выйти из игры", "Продолжить", "Следующий уровень", "Начать заново"
UP, LEFT, DOWN, RIGHT = "UP", "LEFT", "DOWN", "RIGHT"
DIRECTION = [UP, LEFT, DOWN, RIGHT]
UNIFIED_BUTTONS = [MAIN_MENU, QUIT]
MENU_BUTTONS = [PLAY, PICK_LEVEL, UNIFIED_BUTTONS[1]]
PAUSE_BUTTONS = [CONTINUE] + UNIFIED_BUTTONS
PICK_LEVEL_BUTTONS = UNIFIED_BUTTONS

black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')

window_x = 800
window_y = 600

block_size = 30


class Snake:
    speed_default = 15

    def __init__(self, coords):
        self.coords = self.get_coords(coords)
        self.direction = RIGHT
        self.speed = self.speed_default
        self.position = copy.deepcopy(self.coords[0])

    @property
    def len(self):
        return len(self.coords)

    def get_coords(self, coords):
        return [[coord * block_size for coord in pair] for pair in coords]

    def eat_fruit(self, state):
        type = state.food.type
        if type == 'monster':
            self.speed += 5
        if type == 'turtle':
            if self.speed > 5:
                self.speed -= 5
        if type == 'apple':
            state.score += 1
        if type == 'bad_apple':
            self.coords.pop()
        if type == 'star':
            state.score += 3
        if type == 'heart':
            if state.health < 5:
                state.health += 1


class Food:
    def __init__(self):
        self.type = self.random_type
        self.coords = [round(random.randrange(0, window_x - block_size) / block_size) * block_size,
                       round(random.randrange(0, window_y - block_size) / block_size) * block_size]

    def draw_food(self, surface):
        picture = pygame.transform.scale(pygame.image.load(f'{self.type}.png'), (block_size, block_size))
        surface.blit(picture, (self.coords[0], self.coords[1]))

    def reset_food(self):
        self.__init__()

    @property
    def random_type(self):
        apple, monster, turtle, bad_apple, star, heart = 'apple', 'monster', 'turtle', 'bad_apple', 'star', 'heart'
        food_type = [apple, monster, turtle, bad_apple, star, heart]
        return random.choice([type for type in food_type])


class Level:
    def __init__(self, required_len, snake):
        self.required_len = required_len
        self.snake = snake


levels = {"first_level": Level(10, Snake([[10, 5],
                               [9, 5],
                               [8, 5], [7, 5]])),
          "second_level": Level(25, Snake(
              [[1, 3], [1, 2], [1, 1]]))}
levels_list = list(levels.keys())


class State:
    health_default = 3
    score_default = 0
    level_default_name = levels_list[0]

    def __init__(self, picked_level_name=level_default_name):
        self.current_level_name = picked_level_name
        self.current_level_index = levels_list.index(self.current_level_name)
        self.current_level = levels[self.current_level_name]
        self.snake = copy.deepcopy(levels[self.current_level_name].snake)
        self.score = self.score_default
        self.health = self.health_default
        self.food = Food()

    def reset_snake(self):
        self.snake = copy.deepcopy(levels[self.current_level_name].snake)

    def check_state(self, _game):
        if self.health < 1 or self.snake.len < 3:
            pygame.time.delay(100)
            _game.fail(self)
        if self.snake.len >= self.current_level.required_len:
            pygame.time.delay(100)
            _game.win(self)

    def check_next_level(self):
        return self.current_level_index + 1 < len(levels_list)


class Menu:
    def __init__(self, _game):
        self.game = _game

    def menu_mechanism(self, list_of_buttons, draw_menu, selected=0, state=None, color=white):
        menu_exceptions = [self.draw_main_menu, self.draw_pause_menu]
        if state:
            draw_menu(list_of_buttons, state, color, selected)
        else:
            draw_menu(selected)

        pygame.time.wait(200)
        running = True
        pygame.event.clear()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.locals.KEYDOWN:
                    if event.key in [pygame.locals.K_DOWN, pygame.locals.K_s]:
                        selected = (selected + 1) % len(list_of_buttons)
                        if state:
                            draw_menu(list_of_buttons, state, color, selected)
                        else:
                            draw_menu(selected)
                    elif event.key in [pygame.locals.K_UP, pygame.locals.K_w]:
                        selected = (selected - 1) % len(list_of_buttons)
                        if state:
                            draw_menu(list_of_buttons, state, color, selected)
                        else:
                            draw_menu(selected)
                    elif event.key == pygame.locals.K_ESCAPE and \
                            draw_menu not in menu_exceptions and draw_menu != [x for x in menu_exceptions]:
                        self.menu_mechanism(MENU_BUTTONS, self.draw_main_menu)
                    elif event.key == pygame.locals.K_RETURN:
                        if list_of_buttons[selected] == TRY_AGAIN:
                            self.game.run(levels_list[state.current_level_index])
                        if list_of_buttons[selected] == NEXT_LEVEL:
                            if state.check_next_level():
                                self.game.run(levels_list[state.current_level_index+1])
                            else:
                                self.menu_mechanism(MENU_BUTTONS, self.draw_main_menu)
                        if list_of_buttons[selected] == PLAY:
                            self.game.run()
                        if list_of_buttons[selected] == CONTINUE:
                            return
                        if list_of_buttons[selected] in levels_list:
                            self.game.run(levels_list[selected])
                        if list_of_buttons[selected] == PICK_LEVEL:
                            self.menu_mechanism(levels_list + PICK_LEVEL_BUTTONS, self.draw_pick_level_menu)
                        if list_of_buttons[selected] == MAIN_MENU:
                            self.menu_mechanism(MENU_BUTTONS, self.draw_main_menu)
                        if list_of_buttons[selected] == QUIT:
                            exit(0)
                elif event.type == pygame.locals.QUIT:
                    exit(0)

    def draw_main_menu(self, selected=0):
        self.draw_general("Snake Game", MENU_BUTTONS, selected)

    def draw_pick_level_menu(self, selected=0):
        self.draw_general("Choose ur (fighter) level", levels_list + PICK_LEVEL_BUTTONS, selected)

    def draw_pause_menu(self, selected=0):
        self.draw_general("Pause", PAUSE_BUTTONS, selected)

    def draw_general(self, menu_name, list_of_buttons, selected=0):
        self.game.surface.fill(white)
        header_font = pygame.font.SysFont('arial', 70)
        header = header_font.render(menu_name, True, black)
        header_rect = header.get_rect()
        header_rect.midtop = (window_x / 2, window_y / 2 - 100)
        self.game.surface.blit(header, header_rect)
        button_font = pygame.font.SysFont('arial', 40)
        selected_button_font = pygame.font.SysFont('arial', 45)
        for button in range(len(list_of_buttons)):
            if button == selected:
                text = selected_button_font.render(list_of_buttons[button], True, black)
            else:
                text = button_font.render(list_of_buttons[button], True, (100, 100, 100))
            text_rect = text.get_rect()
            text_rect.midtop = (window_x / 2, window_y / 2 + button * 50)
            self.game.surface.blit(text, text_rect)
        pygame.display.update()

    def draw_condition_menu(self, list_of_buttons, state, color, selected=0):
        self.game.surface.fill(black)
        score_font = pygame.font.SysFont('arial', 70)
        score = score_font.render(
            'Your Score is : ' + str(state.score), True, color)
        score_rect = score.get_rect()
        score_rect.midtop = (window_x / 2, window_y / 2 - 100)
        self.game.surface.blit(score, score_rect)
        button_font = pygame.font.SysFont('arial', 40)
        selected_button_font = pygame.font.SysFont('arial', 45)
        for button in range(len(list_of_buttons)):
            if button == selected:
                text = selected_button_font.render(list_of_buttons[button], True, white)
            else:
                text = button_font.render(list_of_buttons[button], True, pygame.Color('gray'))
            text_rect = text.get_rect()
            text_rect.midtop = (window_x / 2, window_y / 2 + button * 50)
            self.game.surface.blit(text, text_rect)
        pygame.display.update()

    def draw_condition_window(self, state, color, selected=0):
        list_of_buttons = UNIFIED_BUTTONS
        if state.check_next_level():
            list_of_buttons = [NEXT_LEVEL] + list_of_buttons
        if color == red:
            list_of_buttons = [TRY_AGAIN] + list_of_buttons
        self.menu_mechanism(list_of_buttons,
                            self.draw_condition_menu, 0, state, color)


class Game:
    fps = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((window_x, window_y + 150))
        self.menu = Menu(self)

        self.menu.menu_mechanism(MENU_BUTTONS, self.menu.draw_main_menu)

    def fail(self, state):
        self.menu.draw_condition_window(state, red)

    def win(self, state):
        self.menu.draw_condition_window(state, green)

    def draw_footer(self, state):
        rect_object = pygame.Rect(0, window_y, window_x, 150)
        pygame.draw.rect(self.surface, white, rect_object)
        font = pygame.font.SysFont('arial', 30)
        health = font.render(f"Health: {state.health}", True, black)
        self.surface.blit(health, (15, window_y + 30))
        score = font.render(f"Score: {state.score}", True, black)
        self.surface.blit(score, (15, window_y + 75))
        pygame.display.update()

    def run(self, picked_level_name=levels_list[0]):
        MOVEMENT = {UP: (0, -block_size), LEFT: (-block_size, 0),
                    DOWN: (0, block_size), RIGHT: (block_size, 0)}
        running = True
        pygame.event.clear()
        state = State(picked_level_name)
        change_to = state.snake.direction

        while running:
            self.fps.tick(state.snake.speed)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        self.menu.menu_mechanism(PAUSE_BUTTONS, self.menu.draw_pause_menu)
                    if event.key in [pygame.locals.K_LEFT, pygame.locals.K_a]:
                        change_to = LEFT
                    elif event.key in [pygame.locals.K_RIGHT, pygame.locals.K_d]:
                        change_to = RIGHT
                    elif event.key in [pygame.locals.K_UP, pygame.locals.K_w]:
                        change_to = UP
                    elif event.key in [pygame.locals.K_DOWN, pygame.locals.K_s]:
                        change_to = DOWN
                if (DIRECTION.index(change_to) + 2) % 4 != DIRECTION.index(state.snake.direction)\
                        and change_to != state.snake.direction:
                    state.snake.direction = change_to

            # штука снизу к нынешнему положению головы прибавляет потенциальное ее перемещение
            # и заменяет большой иф
            state.snake.position = [x+y for x, y in zip(state.snake.position, MOVEMENT[state.snake.direction])]

            if state.snake.position in state.snake.coords:
                state.health -= 1
                state.reset_snake()

            state.snake.coords.insert(0, list(state.snake.position))
            if state.snake.position == state.food.coords:
                state.snake.eat_fruit(state)
                if state.food.type != 'apple':
                    state.snake.coords.pop()
                state.food.reset_food()
            else:
                state.snake.coords.pop()

            self.surface.fill(black)

            state.food.draw_food(self.surface)

            if state.snake.position[0] < 0 or state.snake.position[0] > window_x \
                    or state.snake.position[1] < 0 or state.snake.position[1] > window_y - block_size:
                state.health -= 1
                state.reset_snake()

            for pos in state.snake.coords:
                pygame.draw.rect(self.surface, white,
                                 pygame.Rect(pos[0], pos[1], block_size, block_size))
            state.check_state(self)
            self.draw_footer(state)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()

import copy
import pygame.locals

pygame.display.set_caption('Snake by Monika Veltman')
PLAY, PICK_LEVEL, MAIN_MENU, QUIT, CONTINUE = \
    "Играть", "Выбрать уровень", "Выйти в главное меню", "Выйти из игры", "Продолжить"
UP, LEFT, DOWN, RIGHT = "UP", "LEFT", "DOWN", "RIGHT"
DIRECTION = [UP, LEFT, DOWN, RIGHT]
UNIFIED_BUTTONS = [MAIN_MENU, QUIT]
MENU_BUTTONS = [PLAY, PICK_LEVEL, UNIFIED_BUTTONS[1]]
PAUSE_BUTTONS = [CONTINUE] + UNIFIED_BUTTONS
PICK_LEVEL_BUTTONS = UNIFIED_BUTTONS

black = pygame.Color('black')
white = pygame.Color('white')

window_x = 800
window_y = 600

block_size = 20
MOVEMENT = {UP : (0, -block_size), LEFT : (-block_size, 0), DOWN : (0, block_size), RIGHT : (block_size, 0)}


class Snake:
    speed_default = 15

    def __init__(self, coords):
        self.coords = coords
        self.direction = RIGHT
        self.speed = self.speed_default
        self.position = copy.deepcopy(self.coords[0])

    @property
    def len(self):
        return len(self.coords)


class Level:
    def __init__(self, required_len, snake):
        self.required_len = required_len
        self.snake = snake


levels = {"first_level":
              Level(10, Snake([[10 * block_size, 5 * block_size],
                               [9 * block_size, 5 * block_size],
                               [8 * block_size, 5 * block_size], [7 * block_size, 5 * block_size]])),
          "second_level": Level(25, Snake(
              [[1 * block_size, 3 * block_size], [1 * block_size, 2 * block_size], [1 * block_size, 1 * block_size]]))}
levels_list = list(levels.keys())


class State:
    health_default = 3
    score_default = 0
    level_default = levels_list[0]

    def __init__(self, picked_level=level_default):
        self.current_level = picked_level
        self.current_level_index = list(levels.keys()).index(self.current_level)
        self.snake = copy.deepcopy(levels[self.current_level].snake)
        self.score = self.score_default
        self.health = self.health_default

    def reset_snake(self):
        self.snake = copy.deepcopy(levels[self.current_level].snake)


class Menu:
    def __init__(self, game):
        self.game = game

    def menu_mechanism(self, list_of_buttons, draw_menu, selected=0):
        draw_menu(selected)
        pygame.time.wait(200)
        running = True
        pygame.event.clear()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.locals.KEYDOWN:
                    if event.key in [pygame.locals.K_DOWN, pygame.locals.K_s]:
                        selected = (selected + 1) % len(list_of_buttons)
                        draw_menu(selected)
                    elif event.key in [pygame.locals.K_UP, pygame.locals.K_w]:
                        selected = (selected - 1) % len(list_of_buttons)
                        draw_menu(selected)
                    elif event.key == pygame.locals.K_RETURN:
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
                        if selected == len(list_of_buttons) - 1:
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
        font = pygame.font.SysFont('arial', 80)
        header = font.render(menu_name, True, black)
        header_rect = header.get_rect()
        self.game.surface.blit(header, ((window_x - header_rect.width) / 2, 100))
        button_font = pygame.font.SysFont('arial', 40)
        selected_button_font = pygame.font.SysFont('arial', 45)
        for button in range(len(list_of_buttons)):
            if button == selected:
                text = selected_button_font.render(list_of_buttons[button], True, black)
            else:
                text = button_font.render(list_of_buttons[button], True, (100, 100, 100))
            self.game.surface.blit(text, (200, 200 + button * 50))
        pygame.display.update()


class Game:
    fps = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((window_x, window_y + 150))
        self.menu = Menu(self)

        self.menu.menu_mechanism(MENU_BUTTONS, self.menu.draw_main_menu)

    def draw_footer(self, status):
        rect_object = pygame.Rect(0, window_y, window_x, 150)
        pygame.draw.rect(self.surface, white, rect_object)
        font = pygame.font.SysFont('arial', 30)
        health = font.render(f"Health: {status.health}", True, black)
        self.surface.blit(health, (15, window_y + 30))
        score = font.render(f"Ur mom gay", True, black)
        self.surface.blit(score, (15, window_y + 75))
        pygame.display.update()

    def run(self, picked_level=levels_list[0]):
        running = True
        pygame.event.clear()
        state = State(picked_level)
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

            state.snake.coords.insert(0, list(state.snake.position))
            state.snake.coords.pop()
            self.surface.fill(black)

            if state.snake.position[0] < 0 or state.snake.position[0] > window_x - block_size \
                    or state.snake.position[1] < 0 or state.snake.position[1] > window_y - block_size:
                state.health -= 1
                state.reset_snake()

            for pos in state.snake.coords:
                pygame.draw.rect(self.surface, white,
                                 pygame.Rect(pos[0], pos[1], block_size, block_size))

            if state.health == 0:
                pygame.time.delay(100)
                self.menu.menu_mechanism(MENU_BUTTONS, self.menu.draw_main_menu)
            self.draw_footer(state)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()

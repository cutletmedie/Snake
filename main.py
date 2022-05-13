import copy
import pygame.locals

pygame.display.set_caption('Snake by Monika Veltman')
UNIFIED_BUTTONS = ["Выйти в главное меню", "Выйти из игры"]
MENU_BUTTONS = ["Играть", "Выбрать уровень", UNIFIED_BUTTONS[1]]
PAUSE_BUTTONS = ["Продолжить"] + UNIFIED_BUTTONS
PICK_LEVEL_BUTTONS = ["Хуй"] + UNIFIED_BUTTONS

black = pygame.Color('black')
white = pygame.Color('white')

window_x = 800
window_y = 600

block_size = 20


class Snake:
    speed_default = 15

    def __init__(self, coords):
        self.coords = coords
        self.direction = 'RIGHT'
        self.speed = self.speed_default
        self.position = copy.deepcopy(self.coords[0])

    @property
    def len(self):
        return len(self.coords)


class Level:
    def __init__(self, required_len, snake):
        self.required_len = required_len
        self.snake = snake


levels = {"simple_level":
              Level(10, Snake([[10 * block_size, 5 * block_size], [9 * block_size, 5 * block_size], [8 * block_size, 5 * block_size], [7 * block_size, 5 * block_size]]))}


class Status:
    health_default = 3
    score_default = 0
    level_default = "simple_level"

    def __init__(self, picked_level=level_default):
        self.current_level = picked_level
        self.snake = copy.deepcopy(levels[self.current_level].snake)
        self.score = self.score_default
        self.health = self.health_default

    def reset_snake(self):
        self.snake = copy.deepcopy(levels[self.current_level].snake)


class Game:
    fps = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((window_x, window_y + 150))

        self.mechanism(MENU_BUTTONS, self.draw_main_menu)

    def mechanism(self, list_of_buttons, draw_menu, selected=0):
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
                        if list_of_buttons[selected] == 'Играть':
                            self.run()
                        if list_of_buttons[selected] == 'Выбрать уровень':
                            self.mechanism(PICK_LEVEL_BUTTONS, self.draw_pick_level_menu)
                        if list_of_buttons[selected] == 'Выйти в главное меню':
                            self.mechanism(MENU_BUTTONS, self.draw_main_menu)
                        if selected == len(list_of_buttons) - 1:
                            exit(0)
                elif event.type == pygame.locals.QUIT:
                    exit(0)

    def draw_main_menu(self, selected=0):
        self.draw_general("Snake Game", MENU_BUTTONS, selected)

    def draw_pick_level_menu(self, selected=0):
        self.draw_general("Choose ur (fighter) level", PICK_LEVEL_BUTTONS, selected)

    def draw_general(self, menu_name, list_of_buttons, selected=0):
        self.surface.fill(white)
        font = pygame.font.SysFont('arial', 80)
        header = font.render(menu_name, True, (0, 0, 0))
        header_rect = header.get_rect()
        self.surface.blit(header, ((window_x - header_rect.width) / 2, 100))
        button_font = pygame.font.SysFont('arial', 40)
        selected_button_font = pygame.font.SysFont('arial', 45)
        for button in range(len(list_of_buttons)):
            if button == selected:
                text = selected_button_font.render(list_of_buttons[button], True, (0, 0, 0))
            else:
                text = button_font.render(list_of_buttons[button], True, (100, 100, 100))
            self.surface.blit(text, (200, 200 + button * 50))
        pygame.display.update()

    def draw_footer(self, status):
        rect_object = pygame.Rect(0, window_y, window_x, 150)
        pygame.draw.rect(self.surface, white, rect_object)
        font = pygame.font.SysFont('arial', 30)
        health = font.render(f"Health: {status.health}", True, (0, 0, 0))
        self.surface.blit(health, (15, window_y + 30))
        score = font.render(f"Ur mom gay", True, (0, 0, 0))
        self.surface.blit(score, (15, window_y + 75))
        pygame.display.update()

    def run(self, picked_level="simple_level"):
        running = True
        pygame.event.clear()
        status = Status(picked_level)
        change_to = status.snake.direction

        while running:
            self.fps.tick(status.snake.speed)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.locals.K_LEFT, pygame.locals.K_a]:
                        change_to = 'LEFT'
                    elif event.key in [pygame.locals.K_RIGHT, pygame.locals.K_d]:
                        change_to = 'RIGHT'
                    elif event.key in [pygame.locals.K_UP, pygame.locals.K_w]:
                        change_to = 'UP'
                    elif event.key in [pygame.locals.K_DOWN, pygame.locals.K_s]:
                        change_to = 'DOWN'
                if change_to == 'UP' and status.snake.direction != 'DOWN':
                    status.snake.direction = 'UP'
                if change_to == 'DOWN' and status.snake.direction != 'UP':
                    status.snake.direction = 'DOWN'
                if change_to == 'LEFT' and status.snake.direction != 'RIGHT':
                    status.snake.direction = 'LEFT'
                if change_to == 'RIGHT' and status.snake.direction != 'LEFT':
                    status.snake.direction = 'RIGHT'
            if status.snake.direction == 'UP':
                status.snake.position[1] -= block_size
            elif status.snake.direction == 'DOWN':
                status.snake.position[1] += block_size
            elif status.snake.direction == 'LEFT':
                status.snake.position[0] -= block_size
            elif status.snake.direction == 'RIGHT':
                status.snake.position[0] += block_size

            print(status.snake.coords, 1)
            status.snake.coords.insert(0, list(status.snake.position))
            status.snake.coords.pop()
            self.surface.fill(black)
            print(status.snake.coords, 2)

            if status.snake.position[0] < 0 or status.snake.position[0] > window_x - block_size \
                    or status.snake.position[1] < 0 or status.snake.position[1] > window_y - block_size:
                status.health -= 1
                status.reset_snake()
                print(status.snake.coords, 3)

            for pos in status.snake.coords:
                pygame.draw.rect(self.surface, white,
                                 pygame.Rect(pos[0], pos[1], block_size, block_size))

            if status.health == 0:
                pygame.time.delay(100)
                self.mechanism(MENU_BUTTONS, self.draw_main_menu)
            self.draw_footer(status)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()

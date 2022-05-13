import copy
import pygame.locals

pygame.display.set_caption('Snake by Monika Veltman')
MENU_BUTTONS = ["Играть", "Выбрать уровень", "Выйти"]

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

window_x = 800
window_y = 600


class Snake:
    speed_default = 50

    def __init__(self, coords):
        self.coords = coords
        self.direction = 'RIGHT'
        self.speed = self.speed_default

    @property
    def len(self):
        return len(self.coords)


class Level:
    def __init__(self, required_len, snake):
        self.required_len = required_len
        self.snake = snake


levels = {"simple_level":
              Level(10, Snake([[100, 50], [90, 50], [80, 50], [70, 50]]))}


class Status:
    health_default = 5
    score_default = 0
    level_default = "simple_level"

    def __init__(self, picked_level=level_default):
        self.current_level = picked_level
        self.snake = copy.deepcopy(levels[self.current_level].snake)
        self.score = self.score_default
        self.health = self.health_default


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((window_x, window_y + 150))
        self.surface.fill(black)

        self.mechanism(MENU_BUTTONS, self.draw_main_menu)

    def mechanism(self, list_of_buttons, draw_menu):
        selected = 0
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
                        if selected == 0:
                            self.run()
                        if selected == len(list_of_buttons) - 1:
                            exit(0)
                elif event.type == pygame.locals.QUIT:
                    exit(0)

    def draw_main_menu(self, selected=0):
        self.surface.fill(white)
        font = pygame.font.SysFont('arial', 90)
        header = font.render("Snake Game", True, (0, 0, 0))
        button_font = pygame.font.SysFont('arial', 40)
        selected_button_font = pygame.font.SysFont('arial', 45)
        self.surface.blit(header, (200, 100))
        for button in range(len(MENU_BUTTONS)):
            if button == selected:
                text = selected_button_font.render(MENU_BUTTONS[button], True, (0, 0, 0))
            else:
                text = button_font.render(MENU_BUTTONS[button], True, (100, 100, 100))
            self.surface.blit(text, (200, 200 + button * 50))
        pygame.display.update()

    def draw_footer(self):
        rect_object = pygame.Rect(0, window_y, window_x, 150)
        pygame.draw.rect(self.surface, white, rect_object)
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Ur mom gay", True, (0, 0, 0))
        self.surface.blit(score, (15, window_y + 75))
        pygame.display.update()

    def run(self, picked_level="simple_level"):
        running = True
        pygame.event.clear()
        status = Status(picked_level)
        change_to = status.snake.direction

        snake_position = status.snake.coords[0]
        while running:
            pygame.time.delay(status.snake.speed)
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
                snake_position[1] -= 10
            if status.snake.direction == 'DOWN':
                snake_position[1] += 10
            if status.snake.direction == 'LEFT':
                snake_position[0] -= 10
            if status.snake.direction == 'RIGHT':
                snake_position[0] += 10
            status.snake.coords.insert(0, list(snake_position))
            status.snake.coords.pop()
            self.surface.fill(black)
            for pos in status.snake.coords:
                pygame.draw.rect(self.surface, white,
                                 pygame.Rect(pos[0], pos[1], 10, 10))
            if snake_position[0] < 0 or snake_position[0] > window_x - 10:
                pygame.time.delay(100)
                self.mechanism(MENU_BUTTONS, self.draw_main_menu)
            if snake_position[1] < 0 or snake_position[1] > window_y - 10:
                pygame.time.delay(100)
                self.mechanism(MENU_BUTTONS, self.draw_main_menu)
            self.draw_footer()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()

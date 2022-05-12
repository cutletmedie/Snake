import collections
import pygame.locals

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

window_x = 800
window_y = 600


class Game:
    pygame.display.set_caption('Snake by Monika Veltman')

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((window_x, window_y + 150))
        self.surface.fill(black)

    def run(self):
        running = True
        pygame.event.clear()
        snake = Snake([[100, 50],
                      [90, 50],
                      [80, 50],
                      [70, 50]
                      ])
        change_to = snake.direction

        snake_position = [100, 50]
        snake_body = [[100, 50],
                      [90, 50],
                      [80, 50],
                      [70, 50]
                      ]
        while running:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.locals.K_LEFT, pygame.locals.K_a]:
                        change_to = 'LEFT'
                    elif event.key in [pygame.locals.K_RIGHT, pygame.locals.K_d]:
                        change_to = 'RIGHT'
                    elif event.key in [pygame.locals.K_UP, pygame.locals.K_w]:
                        change_to = 'UP'
                    elif event.key in [pygame.locals.K_DOWN, pygame.locals.K_s]:
                        change_to = 'DOWN'
                if change_to == 'UP' and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                    print(snake.direction)
                if change_to == 'DOWN' and snake.direction != 'UP':
                    snake.direction = 'DOWN'
                    print(snake.direction)
                if change_to == 'LEFT' and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                    print(snake.direction)
                if change_to == 'RIGHT' and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'
                    print(snake.direction)
            if snake.direction == 'UP':
                snake_position[1] -= 10
            if snake.direction == 'DOWN':
                snake_position[1] += 10
            if snake.direction == 'LEFT':
                snake_position[0] -= 10
            if snake.direction == 'RIGHT':
                snake_position[0] += 10
            snake_body.insert(0, list(snake_position))
            snake_body.pop()
            game.surface.fill(black)
            for pos in snake_body:
                pygame.draw.rect(game.surface, white,
                                 pygame.Rect(pos[0], pos[1], 10, 10))
            if snake_position[0] < 0 or snake_position[0] > window_x - 10:
                pygame.time.delay(100)
                pygame.quit()
                quit()
            if snake_position[1] < 0 or snake_position[1] > window_y - 10:
                pygame.time.delay(100)
                pygame.quit()
                quit()
            pygame.display.update()


class Snake:
    def __init__(self, coords):
        self.coords = coords
        self.moves = collections.deque()
        self.direction = 'RIGHT'

    @property
    def len(self):
        return len(self.coords)


if __name__ == "__main__":
    game = Game()
    game.run()

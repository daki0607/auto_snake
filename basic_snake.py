import sys
from pygame.locals import *
import pygame
from random import randint

scale = 50


class Snake(object):
    def __init__(self):
        self.x = 5
        self.y = 5
        # Reference to a function so the snake moves in the same direction
        self.move = self.move_down
        self.body = [(self.x, self.y)]
        self.length = 1

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def update_body(self):
        """ After moving, add on the new head and remove the old tail. """
        self.body = [(self.x, self.y)] + self.body
        self.body.pop()

    def eat(self):
        """ Add another segment to the body. """
        self.body.append((self.x, self.y))
        self.length += 1


class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def spawn_food(cls, width, height):
        """ Randomly spawns food given a width and height. """
        return cls(randint(0, width), randint(0, height))


class Arena(object):
    def __init__(self):
        self.width = 10
        self.height = 10
        self._running = True
        self.snake = Snake()
        self.food = Food.spawn_food(self.width-1, self.height-1)

        self.windowWidth = self.width*scale
        self.windowHeight = self.height*scale
        self._displaySurface = None
        self._snakeImageSurface = None
        self._snakeHeadImageSurface = None
        self._foodImageSurface = None
        self._clock = None

    def _init(self):
        """ Initialize pygame elements. """
        self._running = True

        pygame.init()
        self._clock = pygame.time.Clock()
        self._displaySurface = pygame.display.set_mode(
            (self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        self._snakeImageSurface = pygame.image.load(
            "snake_segment.png").convert()
        self._foodImageSurface = pygame.image.load("food.png").convert()
        self._snakeHeadImageSurface = pygame.image.load(
            "snake_head.png").convert()

    def _render(self):
        """ Redraws the body of the snake and the food. """
        self._displaySurface.fill((0, 0, 0))
        self._displaySurface.blit(
            self._foodImageSurface, (self.food.x*scale, self.food.y*scale))

        for x, y in self.snake.body[1:]:
            self._displaySurface.blit(
                self._snakeImageSurface, (x*scale, y*scale))

        self._displaySurface.blit(
            self._snakeHeadImageSurface,
            (self.snake.x*scale, self.snake.y*scale))

        pygame.display.flip()

    def _update(self):
        """ Move the snake and its body. """
        self.snake.move()
        self.snake.update_body()

    def _collision_check(self):
        """
        Checks for collisions with walls, itself, and food.
        """
        if (self.snake.x > self.width-1
                or self.snake.x < 0
                or self.snake.y > self.height-1
                or self.snake.y < 0):
            self._running = False

        for i in range(1, self.snake.length):
            if (self.snake.body[0] == self.snake.body[i]):
                self._running = False

        if (self.snake.x == self.food.x and self.snake.y == self.food.y):
            self.snake.eat()
            self.food = Food.spawn_food(self.width-1, self.height-1)

    def _stop(self):
        sys.exit()

    def execute(self):
        """ Main loop. """
        self._init()

        while (self._running):
            self._clock.tick(10)
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.snake.move = self.snake.move_right
            if(keys[K_LEFT]):
                self.snake.move = self.snake.move_left
            if (keys[K_UP]):
                self.snake.move = self.snake.move_up
            if (keys[K_DOWN]):
                self.snake.move = self.snake.move_down

            if (keys[K_ESCAPE]):
                self._running = False

            self._update()
            self._collision_check()
            self._render()
        self._stop()


if __name__ == "__main__":
    theGame = Arena()
    theGame.execute()

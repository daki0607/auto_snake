import sys
from pygame.locals import *
import pygame

scale = 50


class Snake(object):
    def __init__(self):
        self.x = 5
        self.y = 5
        self.move = self.move_down

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1


class Arena(object):
    def __init__(self):
        self.snakes = Snake()
        self.width = 10
        self.height = 10
        self.windowWidth = self.width*scale
        self.windowHeight = self.height*scale
        self._running = True
        self._displaySurface = None
        self._imageSurface = None
        self._clock = None

    def _init(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._displaySurface = pygame.display.set_mode(
            (self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._running = True
        self._imageSurface = pygame.image.load("snake_segment.png").convert()

    def _render(self):
        self._displaySurface.fill((0, 0, 0))
        self._displaySurface.blit(
            self._imageSurface, (self.snakes.x*scale, self.snakes.y*scale))
        pygame.display.flip()

    def _update(self):
        self.snakes.move()

    def _collision_check(self):
        """
        Checks for collisions with walls, itself, and food.
        """
        if (self.snakes.x > self.width-1
                or self.snakes.x < 0
                or self.snakes.y > self.height-1
                or self.snakes.y < 0):
            self._running = False

    def _stop(self):
        sys.exit()

    def execute(self):
        self._init()

        while (self._running):
            self._clock.tick(10)
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.snakes.move = self.snakes.move_right
            if(keys[K_LEFT]):
                self.snakes.move = self.snakes.move_left
            if (keys[K_UP]):
                self.snakes.move = self.snakes.move_up
            if (keys[K_DOWN]):
                self.snakes.move = self.snakes.move_down

            if (keys[K_ESCAPE]):
                self._running = False

            self._update()
            self._collision_check()
            self._render()
        self._stop()


if __name__ == "__main__":
    theGame = Arena()
    theGame.execute()

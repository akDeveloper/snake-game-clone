import pygame
from pygame.sprite import Sprite
from pygame import draw
from pygame import Rect, Surface
from controls import Input
from renderer import Renderer
from pygame.math import Vector2

BLOCK = 10

class Level(Sprite):
    def __init__(self, boundaries: list):
        color = (150, 150, 150)
        self.__boundaries = boundaries
        self.__top = Surface((320 - BLOCK, BLOCK))
        self.__top.fill(color)
        self.__left = Surface((BLOCK, 240 - (2 * BLOCK)))
        self.__left.fill(color)
        self.__right = Surface((BLOCK, 240))
        self.__right.fill(color)
        self.__bottom = Surface((320 - BLOCK, BLOCK))
        self.__bottom.fill(color)

    def update(self, time: int) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.__top, self.__boundaries[0])
        renderer.draw(self.__left, self.__boundaries[1])
        renderer.draw(self.__right, self.__boundaries[2])
        renderer.draw(self.__bottom, self.__boundaries[3])

class Food(Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = Surface((BLOCK, BLOCK))
        self.image.fill((200, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        draw.rect(self.image, (200, 100, 100), Rect(0, 0, BLOCK, BLOCK), 1)

    def update(self, time: int) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.image, self.rect, Rect(0, 0, BLOCK, BLOCK))

class Snake(Sprite):
    def __init__(self, screen: tuple, boundaries: list):
        super().__init__()
        self.__is_alive = True
        self.screen: tuple = screen
        self.input: Input = None
        self.speed = BLOCK
        self.image = Surface((BLOCK,  BLOCK)) # Head image
        self.image.fill((100, 100, 100))
        self.body = Surface((BLOCK, BLOCK)) # Body image
        self.body.fill((100, 100, 200))
        self.rect = self.image.get_rect(topleft=(100, 100))
        draw.rect(self.image, (100, 100, 100), Rect(0, 0, BLOCK, BLOCK), 1)
        self.dir_x = 0
        self.dir_y = 0
        self.tail: list = []
        self.tail_length = 1
        self.__boundaries = boundaries

    def set_input(self, input: Input) -> None:
        self.input = input

    def eat(self, food: Rect) -> None:
        self.tail_length += 1

    def update(self, time: int) -> None:
        if self.__is_alive is False:
            return
        dir = self.input.get_direction()
        # Do not go to opposite direction if snake tail is grater than 1
        if dir.x != 0:
            if self.dir_y == 0 and self.dir_x != dir.x and self.tail_length > 1:
                pass
            else:
                self.dir_y = 0
                self.dir_x = dir.x
        elif dir.y != 0:
            if self.dir_x == 0 and self.dir_y != dir.y and self.tail_length > 1:
                pass
            else:
                self.dir_x = 0
                self.dir_y = dir.y

        self.rect.left += self.dir_x * self.speed
        self.rect.top += self.dir_y * self.speed

        # Collide for boundaries
        if self.__collide() is True:
            self.__is_alive = False
            return

        # TODO: Check intersection with its body
        # Decrease tail if the last element of tail is beaten.

        # Game over if intersect with other elements of the body.
        for i, t in enumerate(self.tail):
            if (i == self.tail_length - 1):
                continue
            if t.colliderect(self.rect):
                self.__is_alive = False
                return

        self.tail.append(Rect(self.rect))
        if len(self.tail) > self.tail_length:
            del self.tail[0]

    def draw(self, renderer: Renderer) -> None:
        for t in self.tail:
            if t != self.rect:
                renderer.draw(self.body, t, Rect(0, 0, BLOCK, BLOCK))
            else:
                renderer.draw(self.image, self.rect, Rect(0, 0, BLOCK, BLOCK))

    def is_alive(self) -> bool:
        return self.__is_alive

    def __collide(self) -> bool:
        for b in self.__boundaries:
            if self.rect.colliderect(b):
                return True
        return False

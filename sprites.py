from pygame.sprite import Sprite
from pygame.draw import rect
from pygame import Rect, Surface
from controls import Input
from renderer import Renderer
from pygame.math import Vector2

class Food(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((10, 10))
        self.image.fill((200, 100, 100))
        self.rect = self.image.get_rect(topleft=(200, 100))
        rect(self.image, (200, 100, 100), Rect(0, 0, 10, 10), 1)

    def update(self, time: int) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.image, self.rect, Rect(0, 0, 10, 10))


class Snake(Sprite):
    def __init__(self, screen: tuple):
        super().__init__()
        self.screen: tuple = screen
        self.input: Input = None
        self.speed = 10
        self.image = Surface((10, 10)) # Head image
        self.image.fill((100, 100, 100))
        self.body = Surface((10, 10)) # Body image
        self.body.fill((100, 100, 200))        
        self.rect = self.image.get_rect(topleft=(0, 0))
        rect(self.image, (100, 100, 100), Rect(0, 0, 10, 10), 1)
        self.dir_x = 0
        self.dir_y = 0
        self.tail: list = []

    def set_input(self, input: Input) -> None:
        self.input = input

    def eat(self, food: Rect) -> None:
        self.tail.append(food)

    def update(self, time: int) -> None:
        vel = Vector2(0, 0)
        dir = self.input.get_direction()
        # TODO: Do not go to opposite direction if snake tail is grater than 1
        if dir.x != 0:
            self.dir_y = 0
            self.dir_x = dir.x
        elif dir.y != 0:
            self.dir_x = 0
            self.dir_y = dir.y

        self.rect.left += self.dir_x * self.speed
        self.rect.top += self.dir_y * self.speed

        # TODO: Fix boundaries of level and do not allow to teleport from edges
        if self.rect.right < self.rect.width * -1:
            self.rect.left = self.screen[0]
        elif self.rect.left > self.screen[0]:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = self.screen[1]
        elif self.rect.top > self.screen[1]:
            self.rect.bottom = 0

        # TODO: Check intersection with its body
        # 1. Decrease tail if the last element of tail is beaten.
        # 2. Game over id intersect with other elements of the body.

        self.tail.append(Rect(self.rect))
        if len(self.tail) > 1:
            del self.tail[0]

    def draw(self, renderer: Renderer) -> None:
        for t in self.tail:
            if t != self.rect:
                renderer.draw(self.body, t, Rect(0, 0, 10, 10))
            else:
                renderer.draw(self.image, t, Rect(0, 0, 10, 10))

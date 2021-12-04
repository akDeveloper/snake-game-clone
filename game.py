from pygame import Vector2
from pygame.sprite import collide_rect
from pygame import Rect
from engine import GameState
from controls import Input
from renderer import Renderer
from sprites import Food, Snake
from random import randrange

class LoadState(GameState):
    def __init__(self, renderer: Renderer) -> None:
        super().__init__()
        self.renderer = renderer

    def update(self, time: int, input: Input) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        pass

    def state(self) -> GameState:
        return PlayState(self.renderer)

    def on_event(self, e) -> None:
        pass

class PlayState(GameState):
    def __init__(self, renderer: Renderer):
        self.screen = renderer.screen()
        self.snake = Snake(self.screen)
        self.__create_food()

    def update(self, time: int, input: Input) -> None:
        self.snake.set_input(input)
        if self.snake.rect.colliderect(self.food.rect):
            self.snake.eat(self.food.rect.copy())
            self.__create_food()
        self.snake.update(time)

    def draw(self, renderer: Renderer) -> None:
        self.food.draw(renderer)
        self.snake.draw(renderer)

    def state(self) -> 'GameState':
        return self

    def __create_food(self) -> None:
        rect: Rect = self.__get_random_point()
        # Do not create food over the Snake tail
        while rect.collidelist(self.snake.tail) != -1:
            rect: Rect = self.__get_random_point()
        self.food = Food(rect.left, rect.top)
    
    def __get_random_point(self) -> Rect:
        x = randrange(self.screen[0] - 10)
        y = randrange(self.screen[1] - 10)
        x = round(x / 10, 0) * 10
        y = round(y / 10, 0) * 10
        return Rect(x, y, 10, 10)


    

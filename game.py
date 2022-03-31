from pygame.sprite import collide_rect
from pygame import Rect
from engine import GameState
from controls import Input
from renderer import Renderer
from sprites import Food, Snake, Level
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
        block = 10
        self.renderer = renderer
        self.screen = renderer.screen()
        self.__boundaries = [
            Rect(0, 0, 320 - block, block),
            Rect(0, block, block, 240 - (2 * block)), Rect(320 - block, 0, block, 240),
            Rect(0, 240 - block, 320 - block, block),
        ]
        self.level = Level(self.__boundaries)
        self.snake = Snake(self.screen, self.__boundaries)
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
        self.level.draw(renderer)

    def state(self) -> 'GameState':
        if self.snake.is_alive() is False:
            return PlayState(self.renderer)
        return self

    def __create_food(self) -> None:
        rect: Rect = self.__get_random_point()
        # Do not create food over the Snake tail or Level boundaries
        while rect.collidelist(self.snake.tail) != -1 or rect.collidelist(self.__boundaries) != -1:
            rect: Rect = self.__get_random_point()
        self.food = Food(rect.left, rect.top)

    def __get_random_point(self) -> Rect:
        x = randrange(self.screen[0] - 20)
        y = randrange(self.screen[1] - 20)
        x = round(x / 10, 0) * 10
        y = round(y / 10, 0) * 10
        return Rect(x, y, 10, 10)


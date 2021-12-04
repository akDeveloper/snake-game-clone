from engine import GameState
from controls import Input
from renderer import Renderer
from sprites import Food, Snake

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
        self.snake = Snake(renderer.screen())
        self.food = Food()

    def update(self, time: int, input: Input) -> None:
        self.snake.set_input(input)
        self.snake.update(time)
        if self.snake.rect.colliderect(self.food.rect):
            self.snake.eat(self.food.rect)

    def draw(self, renderer: Renderer) -> None:
        self.snake.draw(renderer)
        self.food.draw(renderer)

    def state(self) -> 'GameState':
        return self

    def __create_food(self) -> None:
        self.food = Food()

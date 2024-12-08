import random
import json
from abc import ABC, abstractmethod
from threading import Thread
import time
from enum import IntEnum
from typing import Callable


class Direction(IntEnum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4


class Game(ABC, Thread):

    def __init__(self) -> None:
        # Thread init
        Thread.__init__(self)
        self.daemon = True
        self.initialized = False
        self.started = False
        self.paused = False
        self.delay = .1
        # Callbacks
        #self.on_start_action: Callable[[str], None] | None = None
        #self.on_pause_action: Callable[[str], None] | None = None
        #self.on_stop_action: Callable[[str], None] | None = None
        self.on_update_action: Callable[[str], None] | None = None
        #self.on_game_over_action: Callable[[str], None] | None = None

    def start_game(self):
        if self.started is False:
            self.started = True
            self.init_game()

    def stop_game(self):
        if self.started:
            self.started = False

    def pause_game(self):
        if self.paused is False:
            self.paused = True

    def resume_game(self):
        if self.paused:
            self.paused = False

    @abstractmethod
    def init_game(self):
        pass

    # def on_start(self, action: Callable[[str], None]) -> None:
    #     self.on_start_action = action

    # def on_pause(self, action: Callable[[str], None]) -> None:
    #     self.on_pause_action = action

    # def on_stop(self, action: Callable[[str], None]) -> None:
    #     self.on_stop_action = action

    def on_update(self, action: Callable[[str], None]) -> None:
        self.on_update_action = action

    # def on_game_over(self, action: Callable[[str], None]) -> None:
    #     self.on_game_over_action = action

    # @abstractmethod
    # def start(self):
    #     pass

    # @abstractmethod
    # def pause(self):
    #     pass

    # @abstractmethod
    # def stop(self):
    #     pass

    @abstractmethod
    def update(self):
        pass

    # @abstractmethod
    # def game_over(self):
    #     pass

    @abstractmethod
    def loop(self) -> None:
        pass

    # Loop forever
    def run(self) -> None:
        while self.is_alive():
            self.loop()
            time.sleep(self.delay)


class Snake(Game):

    def __init__(self, height: int, width: int):
        Game.__init__(self)
        # Board
        self.height = height
        self.width = width
        self.board_size = height * width
        # Snake
        self.snake_indexes = []
        self.snake_direction = 0
        self.snake_speed = 1
        # Fruit
        self.fruit_index = 0
        # Score
        self.score = 0

    def init_game(self) -> None:
        self.snake_indexes = [(self.height + 1) * self.width // 2]
        self.snake_indexes = [self.snake_indexes[0],
                              self.snake_indexes[0] - 1, self.snake_indexes[0] - 2]
        self.snake_direction = Direction.RIGHT
        self.snake_speed = 10
        self.fruit_index = self.get_fruit_index()
        self.update()
        self.initialized = True
        self.started = True

    def get_fruit_index(self) -> int:
        shift = 0
        idx = random.randint(0, self.board_size-len(self.snake_indexes))
        for i in self.snake_indexes:
            if idx <= i:
                shift += 1
        return idx + shift

    def get_coordinates_from_index(self, idx: int) -> tuple[int, int]:
        return idx // self.width, idx % self.width

    def get_index_from_coordinates(self, i: int, j: int) -> int:
        return i * self.width + j

    def loop(self) -> None:
        if self.initialized:
            if self.started and self.paused is False:
                self.move()

    def move(self) -> None:

        head_idx = self.snake_indexes[0]

        i, j = self.get_coordinates_from_index(head_idx)

        match self.snake_direction:
            case Direction.UP:
                i -= 1
            case Direction.DOWN:
                i += 1
            case Direction.LEFT:
                j -= 1
            case Direction.RIGHT:
                j += 1
            case _:
                pass

        new_head_idx = self.get_index_from_coordinates(i, j)

        # Detect collisions
        if self.detect_collision_with_wall(i, j) or self.detect_collision_with_snake_body(new_head_idx):
            self.stop_game()

        if self.started:

            # Eat fruit and grow up
            self.eat_fruit_and_grow_up(new_head_idx)

            # shift all indexes
            self.shift_indexes(new_head_idx)

            # Update rendering
            self.update()

    def detect_collision_with_wall(self, i: int, j: int) -> bool:
        return i < 0 or i >= self.height or j < 0 or j >= self.width

    def detect_collision_with_snake_body(self, head_idx: int) -> bool:
        return head_idx in self.snake_indexes

    def eat_fruit_and_grow_up(self, head_idx: int) -> None:
        if head_idx == self.fruit_index:
            self.snake_indexes.append(0)
            self.fruit_index = self.get_fruit_index()
            self.score += 1

    def shift_indexes(self, head_idx: int):
        i = len(self.snake_indexes) - 1
        while i > 0:
            self.snake_indexes[i] = self.snake_indexes[i-1]
            i -= 1
        self.snake_indexes[0] = head_idx

    def update_direction(self, data: str) -> None:
        if self.started and self.paused is False:
            self.snake_direction = json.loads(data)['direction']

    def get_board_shape(self) -> str:
        return json.dumps({
            'height': self.height,
            'width': self.width
        })

    def update(self) -> None:
        if self.on_update_action is not None:
            self.on_update_action(
                json.dumps({
                    'snakeIndexes': self.snake_indexes,
                    'fruitIndex': self.fruit_index,
                    'score': self.score
                })
            )

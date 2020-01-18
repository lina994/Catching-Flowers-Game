import enum
import math
import random
import time


class Status(enum.Enum):
    run = 1
    pause = 2
    game_over = 3
    terminate = 4


class HorizontalDirection(enum.IntEnum):
    left = -1
    none = 0
    right = 1


class VerticalDirection(enum.IntEnum):
    up = -1
    none = 0
    down = 1


class ImgDirection(enum.Enum):
    left = -1
    right = 1


BG_HEIGHT = 750
BG_WIDTH = 1000
LAND_HEIGHT = 100
LAND_WIDTH = 1000
UNICORN_HEIGHT = 150
UNICORN_WIDTH = 150
PIXIE_HEIGHT = 150
PIXIE_WIDTH = 150
FLOWER_HEIGHT = 50
FLOWER_WIDTH = 50


class GameModel:
    def __init__(self):
        self.status = Status.pause
        self.elements = []
        self.next_time = time.time()  # when we try drop an flower

        # create elements
        self.bg = Background(BG_WIDTH / 2, BG_HEIGHT / 2)
        self.land = Land(BG_WIDTH / 2, BG_HEIGHT - (LAND_HEIGHT / 2))
        self.unicorn = Unicorn(BG_WIDTH / 2, BG_HEIGHT - LAND_HEIGHT - (UNICORN_HEIGHT / 2))
        self.pixie = Pixie(BG_WIDTH / 2, PIXIE_HEIGHT / 2)
        self.text = TextInfo(80, 30)
        self.init_elements()

    def init_elements(self):
        self.elements = []
        self.elements.append(self.bg)
        self.elements.append(self.land)
        self.elements.append(self.unicorn)
        self.elements.append(self.pixie)
        self.elements.append(self.text)

    def add_flower(self):
        flower = Flower(self.pixie.x, self.pixie.y)
        self.elements.append(flower)

    def random_flower_drop(self):  # add flower every 2-4 seconds
        if self.next_time - time.time() < -2:
            self.next_time = time.time() + 2
            self.add_flower()
        elif self.next_time - time.time() < 0:
            if random.uniform(0, 1) < 0.01:
                self.next_time = time.time() + 2
                self.add_flower()

    def check_status(self, element):
        if type(element) is Flower:
            dist = math.sqrt((element.x - self.unicorn.x) ** 2 + (element.y - self.unicorn.y) ** 2)
            if dist < self.unicorn.catch_radius:
                self.text.score += 1
                return False
            elif element.y >= BG_HEIGHT:
                self.text.lives -= 1
                return False
        return True

    def remove_reach_bottom_flowers(self):
        self.elements = [e for e in self.elements if self.check_status(e)]

    def update(self):
        for element in self.elements:
            element.update()
        self.random_flower_drop()
        self.remove_reach_bottom_flowers()

    def change_to_initial_state(self):
        self.init_elements()
        for e in self.elements:
            e.change_to_initial_position()


class GameElement:
    def __init__(self, x, y, direction_x, direction_y, speed):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = speed

    def change_to_initial_position(self):
        self.x = self.initial_x
        self.y = self.initial_y

    def update(self):
        pass


class Background(GameElement):
    def __init__(self, x, y):
        super().__init__(x, y, HorizontalDirection.none, VerticalDirection.none, 0)


class Land(GameElement):
    def __init__(self, x, y):
        super().__init__(x, y, HorizontalDirection.none, VerticalDirection.none, 0)


class Unicorn(GameElement):
    def __init__(self, x, y):
        super().__init__(x, y, HorizontalDirection.none, VerticalDirection.none, speed=6)
        self.catch_radius = (UNICORN_HEIGHT / 2) + (FLOWER_HEIGHT / 2) + 10
        self.img_direction = ImgDirection.left

    def update(self):
        if self.direction_x == HorizontalDirection.left:
            if self.x > 0:
                self.move()
        elif self.direction_x == HorizontalDirection.right:
            if self.x < BG_WIDTH:
                self.move()

    def move(self):
        self.x += self.direction_x * self.speed
        self.direction_x = HorizontalDirection.none


class Pixie(GameElement):
    def __init__(self, x, y):
        super().__init__(x, y, HorizontalDirection.left, VerticalDirection.none, speed=2)

    def update(self):
        self.x += self.direction_x * self.speed
        if self.x <= 0:
            self.x = BG_WIDTH


class Flower(GameElement):
    def __init__(self, x, y):
        super().__init__(x, y, HorizontalDirection.none, VerticalDirection.down, speed=1)

    def update(self):
        self.y += self.direction_y * self.speed


class TextInfo(GameElement):
    def __init__(self, x, y):
        super().__init__(x, y, HorizontalDirection.none, VerticalDirection.none, speed=0)
        self.score = 0
        self.lives = 3

    def change_to_initial_position(self):
        self.score = 0
        self.lives = 3
        super().change_to_initial_position()


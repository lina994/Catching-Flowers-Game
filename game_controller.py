from game_model import *


class GameController:
    def __init__(self, model):
        self.model = model
        pass

    def start_new_game(self):
        self.model.change_to_initial_state()
        self.model.status = Status.run

    def continue_game(self):
        self.model.status = Status.run

    def exit_game(self):
        self.model.status = Status.terminate

    def press_left(self, event):
        self.model.unicorn.direction_x = HorizontalDirection.left
        self.model.unicorn.img_direction = ImgDirection.left

    def press_right(self, event):
        self.model.unicorn.direction_x = HorizontalDirection.right
        self.model.unicorn.img_direction = ImgDirection.right

    def press_p(self, event):
        if self.model.status == Status.run:
            self.model.status = Status.pause

    def update_model(self):
        if self.model.status == Status.run:
            self.model.update()






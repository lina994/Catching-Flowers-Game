from game_model import GameModel
from game_controller import GameController
from game_view import GameView


def main():
    # MVC pattern (Model View Controller)
    model = GameModel()
    controller = GameController(model)
    view = GameView(model, controller)


if __name__ == "__main__":
    main()



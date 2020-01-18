import tkinter as tk
from PIL import ImageTk, Image

from game_model import *


class GameImages:
    def __init__(self):
        # background
        self.bg_pil_img = Image.open('./resources/bg.png')
        self.bg_img = ImageTk.PhotoImage(self.bg_pil_img)

        # land
        self.land_pil_img = Image.open('./resources/land.png')
        self.land_img = ImageTk.PhotoImage(self.land_pil_img)

        # unicorn
        self.unicorn_pil_img = Image.open('./resources/unicorn.png')
        self.unicorn_pil_img_right = self.unicorn_pil_img.resize((UNICORN_HEIGHT, UNICORN_WIDTH))
        self.unicorn_pil_img_left = self.unicorn_pil_img_right.transpose(Image.FLIP_LEFT_RIGHT)
        self.unicorn_img_right = ImageTk.PhotoImage(self.unicorn_pil_img_right)
        self.unicorn_img_left = ImageTk.PhotoImage(self.unicorn_pil_img_left)

        # pixie
        self.pixie_pil_img = Image.open('./resources/pixie.png')
        self.pixie_pil_img = self.pixie_pil_img.resize((PIXIE_HEIGHT, PIXIE_WIDTH))
        self.pixie_img = ImageTk.PhotoImage(self.pixie_pil_img)

        # flower
        self.flower_pil_img = Image.open('./resources/flower.png')
        self.flower_pil_img = self.flower_pil_img.resize((FLOWER_HEIGHT, FLOWER_WIDTH))
        self.flower_img = ImageTk.PhotoImage(self.flower_pil_img)

    def get_image(self, element):
        if type(element) is Background:
            return self.bg_img
        if type(element) is Land:
            return self.land_img
        if type(element) is Unicorn:
            if element.img_direction == ImgDirection.left:
                return self.unicorn_img_left
            else:
                return self.unicorn_img_right
        if type(element) is Pixie:
            return self.pixie_img
        if type(element) is Flower:
            return self.flower_img
        return None


class DisplayGame:
    def __init__(self, canvas, _id):
        self.canvas = canvas
        self.id = _id

    def delete_from_screen(self):
        self.canvas.delete(self.id)


class DisplayGameImage(DisplayGame):
    def __init__(self, canvas, element, img):
        super().__init__(canvas, canvas.create_image(element.x, element.y, image=img))


class DisplayGameText(DisplayGame):
    def __init__(self, canvas, element):
        text = "Score: %d\nLives: %d" % (element.score, element.lives)
        super().__init__(canvas, canvas.create_text(element.x, element.y, font='12', text=text))


class DisplayMenu(DisplayGame):
    def __init__(self, root, canvas, controller):
        menu = tk.Frame(root, bg='grey', width=400, height=40)
        menu.pack(fill='x')
        new_game = tk.Button(menu, text="New Game", width=15, height=2, font='12', command=controller.start_new_game)
        new_game.pack(side="top")
        continue_game = tk.Button(menu, text="Continue", width=15, height=2, font='12', command=controller.continue_game)
        continue_game.pack(side="top")
        exit_game = tk.Button(menu, text="Exit Game", width=15, height=2, font='12', command=controller.exit_game)
        exit_game.pack(side="top")
        _id = canvas.create_window(BG_WIDTH / 2, BG_HEIGHT / 2, window=menu)
        super().__init__(canvas, _id)


class GameView:
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

        # root
        self.root = tk.Tk()
        self.root.title('Catching Flowers Game')

        # load images files
        self.images = GameImages()

        # canvas
        self.canvas = tk.Canvas(self.root, width=BG_WIDTH, height=BG_HEIGHT)
        self.canvas.pack()
        self.root.update()

        # canvas elements id
        self.elements_id = []
        self.add_elements_to_canvas()

        self.add_event_handlers()
        self.is_menu_open = False

        self.draw()
        self.root.mainloop()

    def add_elements_to_canvas(self):
        for e in self.model.elements:
            if type(e) is TextInfo:
                self.elements_id.append(DisplayGameText(self.canvas, e))
            else:
                self.elements_id.append(DisplayGameImage(self.canvas, e, self.images.get_image(e)))
        if self.model.status == Status.pause or self.model.status == Status.game_over:
            self.elements_id.append(DisplayMenu(self.root, self.canvas, self.controller))
            self.is_menu_open = True

    def add_event_handlers(self):
        self.root.bind("<Left>", self.controller.press_left)
        self.root.bind("<Right>", self.controller.press_right)
        self.root.bind("p", self.controller.press_p)

    def draw(self):
        self.controller.update_model()
        if self.model.status == Status.run or not self.is_menu_open:
            self.is_menu_open = False
            self.canvas.delete("all")
            self.add_elements_to_canvas()
        if self.model.status == Status.terminate:
            self.root.destroy()
        else:
            self.canvas.after(5, self.draw)

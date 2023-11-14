import numpy as np
import cv2
import time
from tkinter import *
from PIL import Image
from PIL import ImageTk
from send import post, IMG_DIR
from merge import merge
# import RPi.GPIO as g


class Window(Tk):
    i = 0
    pw = ''
    images = []
    start_time = time.time()
    cam = cv2.VideoCapture(0)
    fps = cam.get(cv2.CAP_PROP_FPS)
    delay = round(1000.0/fps)
    button_down = False
    button_up = False

    def __init__(self) -> None:
        super().__init__()
        self.attributes("-fullscreen", True)
        self.overrideredirect(True)
        self.bind("<Escape>", lambda e: self.quit())
        self.frames = [Frame(self), Frame(self), Frame(self)]
        for frame in self.frames:
            frame.grid(row=0, column=0, sticky="nsew")
        self.change_screen(0)
        self.init_first()
        self.init_second()
        self.init_third()

    def init_first(self) -> None:

        def input_pw(event) -> None:
            self.pw = textfield.get()
            self.start_time = time.time()
            self.change_screen(1)
            self.bind("<space>", lambda e: self.get_frame(save=True))

        main_text = Label(self.frames[0], text="다운로드시 필요한\n비밀번호를 알려주세요")
        sub_text = Label(self.frames[0], text="PIN번호를 복구하지 못하니 신중히 정해주세요!")
        textfield = Entry(self.frames[0])
        textfield.bind("<Return>", input_pw)

        main_text.pack(side=TOP)
        sub_text.pack(side=TOP)
        textfield.pack(side=TOP)

    def init_second(self) -> None:

        def stream() -> None:
            if self.screen == 1:
                timer = int(150 + self.start_time - time.time())
                count = len(self.images) + 1

                if (timer == 0 or count == 5):
                    merge(self.i, *self.images)
                    post(self.i, self.pw)
                    self.change_screen(2)
                    self.unbind("<space>")
                    self.start_time = time.time()

                if self.button_down and self.button_up:
                    img = self.get_frame(save=True)
                else:
                    img = self.get_frame()

                timer_label.configure(text=f"{timer}")
                count_label.configure(text=f"{count}/4")
                cam_view.configure(image=img)
                cam_view.image = img

            self.after(self.delay, stream)

        timer = int(150 + self.start_time - time.time())
        count = len(self.images) + 1
        img = self.get_frame()

        timer_label = Label(self.frames[1], text=f"{timer}")
        count_label = Label(self.frames[1], text=f"{count}/4")
        cam_view = Label(self.frames[1], image=img)
        cam_view.image = img

        cam_view.pack(side=LEFT)
        timer_label.pack(side=TOP)
        count_label.pack(side=TOP)

        stream()

    def init_third(self) -> None:

        def stream() -> None:
            if self.screen == 2:
                timer = int(time.time() - self.start_time)

                if timer >= 5:
                    for child in self.frames[0].winfo_children():
                        child.destroy()
                    self.init_first()
                    self.change_screen(0)
                    self.i += 1
                    self.pw = ''
                    self.images = []

                id_num.configure(text=f"{self.i}")
                pw_num.configure(text=f"{self.pw}")

            self.after(self.delay, stream)

        main_text = Label(self.frames[2], text="사진 촬영이\n완료되었습니다")
        sub_text = Label(self.frames[2], text="고유 번호와 비밀번호를 꼭 기억해주세요")

        id_row = Frame(self.frames[2])
        id_text = Label(id_row, text="고유번호")
        id_num = Label(id_row, text=f"{self.i}")
        id_text.pack(side=LEFT)
        id_num.pack(side=RIGHT)

        pw_row = Frame(self.frames[2])
        pw_text = Label(pw_row, text="비밀번호")
        pw_num = Label(pw_row, text=f"{self.pw}")
        pw_text.pack(side=LEFT)
        pw_num.pack(side=RIGHT)

        main_text.pack(side=TOP)
        sub_text.pack(side=TOP)
        id_row.pack(side=TOP)
        pw_row.pack(side=TOP)

        stream()

    def change_screen(self, index: int) -> None:
        self.screen = index
        frame: Frame = self.frames[index]
        frame.tkraise()

    def get_frame(self, save=False) -> PhotoImage:
        ret, img = self.cam.read()
        if save:
            self.images.append(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 300))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        return img


window = Window()

window.mainloop()

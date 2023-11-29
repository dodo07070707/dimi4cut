import cv2
import time
from tkinter import *
from PIL import Image
from PIL import ImageTk
from send import post
from merge import merge
import RPi.GPIO as g
import time
import spidev
import numpy as np

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
# GPIO 설정
button_pin = 17  # 버튼 핀
buzzer_pin = 18  # 부저 핀
segment_pins = (21, 20, 16, 12, 25, 24, 22, 23)  # 7-Segment 핀
led_pin = 26  # LED 핀
triger = 2 #초음파 센서 핀
echo = 3
pins = {'pin_R':11, 'pin_G':9, 'pin_B':10} #RGB LED 핀


# GPIO 초기화
g.setwarnings(False)
g.setmode(g.BCM)
g.setup(button_pin, g.IN, pull_up_down=g.PUD_UP)
g.setup(buzzer_pin, g.OUT)
g.setup(segment_pins, g.OUT)
g.setup(led_pin, g.OUT)
g.setup(echo, g.IN)
g.setup(triger, g.OUT)

buzzerpwm = g.PWM(buzzer_pin, 1000)
# 7-Segment Display 디지트 맵
digit_map = {
    '0' : (1, 1, 1, 1, 1, 1, 0, 0),
    '1' : (0, 1, 1, 0, 0, 0, 0, 0),
    '2' : (1, 1, 0, 1, 1, 0, 1, 0),
    '3' : (1, 1, 1, 1, 0, 0, 1, 0),
    '4' : (0, 1, 1, 0, 0, 1, 1, 0),
    '5' : (1, 0, 1, 1, 0, 1, 1, 0),
    '6' : (1, 0, 1, 1, 1, 1, 1, 0),
    '7' : (1, 1, 1, 0, 0, 1, 0, 0),
    '8' : (1, 1, 1, 1, 1, 1, 1, 0),
    '9' : (1, 1, 1, 1, 0, 1, 1, 0),
    '.' : (0, 0, 0, 0, 0, 0, 0, 0),
}

colors = [0xFF0000, 0x0000FF]

for i in pins:
    g.setup(pins[i], g.OUT)
    g.output(pins[i], g.HIGH)
p_R = g.PWM(pins['pin_R'], 2000)
p_G = g.PWM(pins['pin_G'], 2000)
p_B = g.PWM(pins['pin_B'], 2000)
p_R.start(0)
p_G.start(0)
p_B.start(0)

# text 430:1080 = 43:108
# frame 864:1080 = 4:5
rate = 1


def px2fh(px):  # convert px to font-size
    return int(px / 108 * 43 * rate)


def px2h(px):  # convert px to frame-size
    return px * 0.8 * rate


class SpacingText(Frame):  # text with line-spacing
    def __init__(self, master, font, text, spacing=px2h(3), height=None, bg='black', fg='white') -> None:
        super().__init__(master, bg=bg, height=height)
        self.text = text
        self.font = font
        self.spacing = spacing
        self.bg = bg
        self.fg = fg
        self.draw()

    def draw(self):
        line = Frame(self, bg=self.bg, pady=0)
        line.pack(side=TOP)
        for char in self.text:
            enter = False
            if char == '\n':
                char = ' '
                enter = True
            Label(
                line,
                text=char,
                font=self.font,
                bg=self.bg,
                fg=self.fg,
                padx=self.spacing/2,
                pady=0,
            ).pack(side=LEFT)
            if enter:
                line = Frame(self, bg=self.bg, pady=0)
                line.pack(side=TOP)


# custom text
class CustomText(Label):
    def __init__(self, master, font, text, bg='black', fg='white') -> None:
        super().__init__(master, bg=bg, fg=fg, font=font, text=text)


#  text|number
class InfoRow(Frame):
    def __init__(self, master, text, value):
        super().__init__(
            master,
            width=px2h(434),
            height=px2h(64),
            bg='black',
        )
        self.info_text = SpacingText(
            self,
            text=text,
            font=f'Pretendard {px2fh(50)} bold',
            spacing=px2h(1.92),
        )
        self.box1 = Frame(self, width=px2h(53), bg='black')
        self.line = Frame(self, width=px2h(1), height=60, bg='#D9D9D9')
        self.box2 = Frame(self, width=px2h(43), bg='black')
        self.info_num_box = Frame(
            self,
            width=px2h(158),
            height=px2h(64),
            bg='black'
        )
        self.info_num_box.pack_propagate(False)
        self.info_num = SpacingText(
            self.info_num_box,
            text=f"{value}",
            font=f'Pretendard {px2fh(64)} bold',
            spacing=px2h(1.92),
        )
        self.info_text.pack(side=LEFT)
        self.box1.pack(side=LEFT)
        self.line.pack(side=LEFT)
        self.box2.pack(side=LEFT)
        self.info_num_box.pack(side=TOP)
        self.info_num.pack(side=TOP, pady=(px2h(64)-px2fh(64))/2)


# send image to server
def image_upload(user_id, pw, images):
    merge(*images)
    post(user_id, pw)


# main object(GUI window)
class Window(Tk):
    i = 0
    pw = ''
    images = []
    screen = 0
    full = True
    start_time = time.time()
    cam = cv2.VideoCapture(0)
    fps = cam.get(cv2.CAP_PROP_FPS)
    delay = round(1000.0/fps)  # microsecond per frame
    button_down = False
    button_up = False

    def __init__(self) -> None:
        super().__init__()
        self.attributes("-fullscreen", True)
        self.bind('<F11>', lambda e: self.change_full())
        self.screens = [Frame(self), Frame(self), Frame(self)]
        self.change_screen(0)

    def change_full(self):
        self.full = not self.full
        self.attributes("-fullscreen", self.full)

    # first page

    def render_first(self) -> None:
        def input_pw(event) -> None:
            if len(textfield.get()) == 4:
                self.pw = textfield.get()
                self.start_time = time.time()
                # move to second page
                self.change_screen(1)

        # increase user id
        self.i += 1

        self.pw = ''
        box1 = Frame(self.screens[0], height=px2h(272), bg='black')
        main_text = SpacingText(
            self.screens[0],
            text="다운로드시 필요한\n비밀번호를 알려주세요",
            font=f'Pretendard {px2fh(72)} bold',
            spacing=px2h(2.16),
            height=px2h(174),
        )
        sub_text = SpacingText(
            self.screens[0],
            text="\nPIN번호를 복구하지 못하니 신중히 정해주세요!",
            font=f'Pretendard {px2fh(36)} bold',
            fg='grey',
            spacing=px2h(1.08),
            height=px2h(94),
        )
        box2 = Frame(self.screens[0], height=px2h(124), bg='black')

        # check password is valid
        vcmd = (
            self.screens[0].register(
                lambda x: (len(x) <= 4 and x.isdigit()) or x == ''
            ),
            '%P',
        )
        textfield = Entry(
            self.screens[0],
            width=4,
            font=f'Pretendard {px2fh(72)} bold',
            bg='black',
            fg='white',
            borderwidth=0,
            validate="key",
            validatecommand=vcmd,
        )
        textfield.bind("<Return>", input_pw)
        line1 = Frame(
            self.screens[0],
            height=0.8*rate,
            width=px2h(515),
            bg='#D9D9D9'
        )

        box1.pack(side=TOP)
        main_text.pack(side=TOP)
        sub_text.pack(side=TOP)
        box2.pack(side=TOP)
        textfield.pack(side=TOP)
        line1.pack(side=TOP)
        # set initial focus
        textfield.focus_set()

    def render_second(self) -> None:
        self.images = []

        def stream() -> None:  # recursive function(main loop)
            timer = int(20 + self.start_time - time.time())
            count = len(self.images) + 1

            if (timer == 0 or count == 5):
                for loop in range(8):
                    g.output(segment_pins[loop], digit_map['.'][loop])
                #self.unbind("<space>")
                self.change_screen(2)  # move to third page
                return
            
            if g.input(button_pin)==g.LOW:
                self.button_down=True
            
            if self.button_down and g.input(button_pin)==g.HIGH:
                self.button_up = True

            # when button-pressed
            if self.button_down and self.button_up:
                self.button_down = False
                self.button_up = False
                # save image
                img = self.get_frame(save=True)
            else:
                img = self.get_frame()
                
            if timer < 10:
                for loop in range(8):
                    g.output(segment_pins[loop], digit_map[str(timer)][loop])

            # update GUI
            timer_label.configure(text=f"{timer}초")
            count_label.configure(text=f"{count}/4")
            cam_view.configure(image=img)
            cam_view.image = img

            # recurse after delay
            self.after(self.delay, stream)

        #self.bind("<space>", lambda e: self.get_frame(save=True))
        timer = int(150 + self.start_time - time.time())
        count = len(self.images) + 1
        img = self.get_frame()

        box1 = Frame(self.screens[1], height=px2h(279), bg='black')
        timer_label = CustomText(
            self.screens[1],
            text=f"{timer}초",
            font=f'Pretendard {px2fh(100)} bold',
        )
        box2 = Frame(self.screens[1], height=px2h(272), bg='black')
        count_label = CustomText(
            self.screens[1],
            text=f"{count}/4",
            font=f'Pretendard {px2fh(100)} bold',
        )
        box3 = Frame(self.screens[1], width=px2h(138), bg='black')
        cam_view = Label(
            self.screens[1],
            image=img,
            bg='black',
        )
        cam_view.image = img

        box3.pack(side=LEFT)
        cam_view.pack(side=LEFT)
        box1.pack(side=TOP)
        timer_label.pack(side=TOP)
        box2.pack(side=TOP)
        count_label.pack(side=TOP)

        # start loop
        stream()

    def render_third(self) -> None:  # recursive function(main loop)
        self.upload_completed = False

        def stream() -> None:
            if not self.upload_completed:
                self.upload_completed = True
                # draw on window
                self.update()
                # upload image
                image_upload(self.i, self.pw, self.images)
                self.pw = 'abcd'

            timer = int(time.time() - self.start_time)

            # wait 5 sec
            if timer >= 5:
                # move to first page
                self.change_screen(0)
                return

            # recurse after delay
            self.after(self.delay, stream)

        self.start_time = time.time()

        box1 = Frame(self.screens[2], bg='black', height=px2h(263))
        main_text = SpacingText(
            self.screens[2],
            text="사진 촬영이\n완료되었습니다",
            font=f'Pretendard {px2fh(72)} bold',
            spacing=px2h(2.16),
            height=px2h(174),
        )
        box2 = Frame(self.screens[2], bg='black', height=px2h(67))
        sub_text = SpacingText(
            self.screens[2],
            text="고유 번호와 비밀번호를 꼭 기억해주세요",
            font=f'Pretendard {px2fh(36)} bold',
            fg='grey',
            spacing=px2h(1.08),
        )
        box3 = Frame(self.screens[2], bg='black', height=px2h(125))

        id_row = InfoRow(self.screens[2], '고유번호', self.i)

        box4 = Frame(self.screens[2], bg='black', height=px2h(19))

        pw_row = InfoRow(self.screens[2], '비밀번호', self.pw)

        box1.pack(side=TOP)
        main_text.pack(side=TOP)
        box2.pack(side=TOP)
        sub_text.pack(side=TOP)
        box3.pack(side=TOP)
        id_row.pack(side=TOP)
        box4.pack(side=TOP)
        pw_row.pack(side=TOP)

        # start loop
        stream()

    # move page
    def change_screen(self, index: int) -> None:
        # destroy current page
        for child in self.screens[self.screen].winfo_children():
            child.destroy()
        self.screens[self.screen].destroy()

        self.screen = index

        # draw new page
        self.screens[index] = Frame(
            self, width=1920*rate, height=1080*rate, bg='black')
        self.screens[index].pack(fill=BOTH, expand=1)
        if index == 0:
            self.render_first()
        elif index == 1:
            self.render_second()
        elif index == 2:
            self.render_third()

    def get_frame(self, save=False) -> PhotoImage:
        # get frame
        ret, img = self.cam.read()

        if save == True:
            self.images.append(img)

        # convert image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (int(px2h(1200)), int(px2h(900))))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        return img


# make GUI window
window = Window()
window.geometry(f"{1920*rate}x{1080*rate}")

# start window
window.mainloop()


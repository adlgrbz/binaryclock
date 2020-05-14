from os import path
from tkinter import *
from datetime import datetime
from tkinter import colorchooser
from configparser import ConfigParser
from tkinter import messagebox as mbox


__version__ = "2.0"
__author__ = "Adil Gürbüz"
__contact__ = "adlgrbz@tutamail.com"
__source__ = "https://github.com/adlgrbz/binaryclock"

this_dir, this_filename = path.split(__file__)


class Clock(Tk):
    def __init__(self):
        super().__init__()
        self.icon = PhotoImage(file=f"{this_dir}/data/binaryclock.gif")
        self.wm_iconphoto(self._w, self.icon)

        self.configp = ConfigParser()
        self.configp.read(f"{this_dir}/data/config.ini")

        self.lamp_color = self.configp["default"]["lamp_color"]  # "#306998"
        self.bg_color = self.configp["default"]["bg_color"]  # "#D9D9D9"
        self.text_color = self.configp["default"]["text_color"]  # "#000000"

        self.config(bg=self.bg_color)

        # self.tm_status = bool(int(self.configp["default"]["top_most"]))
        # self.or_status = bool(int(self.configp["default"]["override_redirect"]))

        # self.wm_attributes("-topmost", self.tm_status)
        # self.overrideredirect(self.or_status)

        self.frame_list = []
        frame_names = ["Hour", "Minute", "Second"]

        self.hour_lamps = []
        self.minute_lamps = []
        self.second_lamps = []

        self.lamp_list = [self.hour_lamps, self.minute_lamps, self.second_lamps]

        for name in range(3):
            self.frame_list.append(LabelFrame(self, text=frame_names[name]))
            self.frame_list[name].config(padx=5, pady=5)
            self.frame_list[name].grid(row=0, column=name, padx=5, pady=5)

        [
            _.config(bg=self.bg_color, fg=self.text_color)
            for _ in self.frame_list
        ]

        for i in range(3):
            self.place_lamps(self.lamp_list[i], self.frame_list[i])

        self.main()

    def main(self):
        self.popup_menu()
        self.update_hour()
        self.update_minute()
        self.update_second()

    def place_lamps(self, l, f):
        index = 0
        for y in range(4):
            for lampx in range(2):
                l.append(Label(f))
                l[index].config(
                    bg=(self.bg_color), width=2, height=1, relief=FLAT
                )
                l[index].grid(row=y, column=lampx, padx=1, pady=1)

                index += 1

    def update_hour(self):
        h = self.get_time()[0]
        self.place_colors(self.hour_lamps, h)
        self.frame_list[0].after(1000, self.update_hour)

    def update_minute(self):
        m = self.get_time()[1]
        self.place_colors(self.minute_lamps, m)
        self.frame_list[1].after(1000, self.update_minute)

    def update_second(self):
        s = self.get_time()[2]
        self.place_colors(self.second_lamps, s)
        self.frame_list[2].after(1000, self.update_second)

    def place_colors(self, lamp_list, time):
        binary_numbers = self.dec_to_bin(time)
        i = 0

        for b in binary_numbers:
            if b == "1":
                lamp_list[i]["bg"] = self.lamp_color
            else:
                lamp_list[i]["bg"] = self.bg_color

            i += 1

    def dec_to_bin(self, num):
        s1, s2 = [bin(int(num[i]))[2:] for i in range(2)]

        if len(s1) < 4:
            zero = 4 - len(s1)
            s1 = zero * "0" + s1
        if len(s2) < 4:
            zero = 4 - len(s2)
            s2 = zero * "0" + s2

        unified = ""

        for i in list(zip(s1, s2)):
            unified += str(i[0]) + str(i[1])

        return unified

    def get_time(self):
        time = datetime.now().strftime("%H.%M.%S")
        return time.split(".")

    def popup_menu(self):
        self.popup = Menu(self, tearoff=0)

        self.popup.add_command(label="Configure", command=(self.configure))
        self.popup.add_command(label="About", command=(self.about))
        self.popup.add_separator()
        self.popup.add_command(label="Exit", command=lambda: aw.destroy())

        self.bind("<Button-3>", self.show_popup_menu)

    def show_popup_menu(self, e):
        try:
            self.popup.tk_popup(e.x_root, e.y_root, 0)
        finally:
            self.popup.grab_release()

    def configure(self):
        cw = Toplevel()
        cw.title("Settings")
        cw.config(padx=5, pady=5)
        cw.resizable(0, 0)
        cw.wm_iconphoto(cw._w, self.icon)

        def change_lamp_color():
            rgb = colorchooser.askcolor()[1]
            if rgb == None:
                return

            lc_button["bg"] = rgb
            self.lamp_color = rgb
            self.update_hour()
            self.update_minute()
            self.update_second()
            self.save_config(lamp_color=rgb)

        def change_text_color():
            rgb = colorchooser.askcolor()[1]
            if rgb == None:
                return

            tc_button["bg"] = rgb
            self.text_color = rgb
            [_.config(fg=rgb) for _ in self.frame_list]
            self.save_config(text_color=rgb)

        def change_background_color():
            rgb = colorchooser.askcolor()[1]
            if rgb == None:
                return

            bgc_button["bg"] = rgb
            self.bg_color = rgb
            self.config(bg=self.bg_color)
            [_.config(bg=rgb) for _ in self.frame_list]
            self.save_config(bg_color=rgb)

        # def change_top_most():
        #     tm_label["text"] = f"Top Most ({not self.tm_status}):"
        #     self.save_config(text_color=int(not self.tm_status))
        #     mbox.showinfo("Info", "Restart the software!")

        # def change_override_redirect():
        #     or_label["text"] = f"Override Redirect ({not self.or_status}):"
        #     self.save_config(text_color=int(not self.or_status))
        #     mbox.showinfo("Info", "Restart the software!")

        lc_label = Label(cw, text="Lamp Color:").grid(row=0, column=0, sticky=W)
        lc_button = Button(cw, bg=self.lamp_color, command=change_lamp_color)
        lc_button.grid(row=0, column=1, sticky=W + E)

        tc_label = Label(cw, text="Text Color:").grid(row=1, column=0, sticky=W)
        tc_button = Button(cw, bg=self.bg_color, command=change_text_color)
        tc_button.grid(row=1, column=1, sticky=W + E)

        bgc_label = Label(cw, text="Background Color:").grid(
            row=2, column=0, sticky=W
        )
        bgc_button = Button(
            cw, bg=self.bg_color, command=change_background_color
        )
        bgc_button.grid(row=2, column=1, sticky=W + E)

        # tm_label = Label(cw)
        # tm_label["text"] = f"Top Most ({self.tm_status}):"
        # tm_label.grid(row=3, column=0, sticky=W)
        # tm_button = Button(cw, text="Change", command=change_top_most)
        # tm_button.grid(row=3, column=1)

        # or_label = Label(cw)
        # or_label["text"] = f"Override Redirect ({self.or_status}):"
        # or_label.grid(row=4, column=0, sticky=W)
        # or_button = Button(cw, text="Change", command=change_override_redirect)
        # or_button.grid(row=4, column=1)

        Button(cw, text="Close", command=lambda: cw.destroy()).grid(
            row=5, column=1, pady=(25, 0), sticky=W + E,
        )

    def about(self):
        aw = Toplevel()
        aw.title("About")
        aw.resizable(0, 0)
        aw.wm_iconphoto(aw._w, self.icon)

        Label(
            aw,
            text=f"{self.wm_title()} {__version__}",
            compound=LEFT,
            image=self.icon,
        ).pack(padx=5, pady=5)
        info_text = (
            f"Author: {__author__}\n"
            f"Contact: {__contact__}\n\n"
            f"Source: {__source__}"
        )
        Label(aw, text=info_text, padx=5, pady=5, relief=RIDGE).pack()

        Button(aw, text="Close", command=lambda: aw.destroy()).pack(
            padx=5, pady=5, side=RIGHT
        )

    def save_config(self, *args, **kwargs):
        key, value = list(kwargs.items())[0]
        self.configp["default"][key] = value

        with open(f"{this_dir}/data/config.ini", "w") as file:
            self.configp.write(file)

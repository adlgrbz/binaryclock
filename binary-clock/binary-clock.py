#!/usr/bin/python3

"""
Binary Clock with Tkinter
Date: 06 Sep 2019
Author: Adil Gürbüz
Mail: adlgrbz@protonmail.com
"""

from tkinter import *
from datetime import datetime

class Template(Tk):
    def __init__(self):
        super().__init__()
        
        #           H-H    M-M    S-S
        #          +-+-+  +-+-+  +-+-+
        #  2^3= 8  |1|2|  |1|2|  |1|2|
        #  2^2= 4  |3|4|  |3|4|  |3|4|
        #  2^1= 2  |5|6|  |5|6|  |5|6|
        #  2^0= 1  |7|8|  |7|8|  |7|8|
        #          +-+-+  +-+-+  +-+-+

        #Sample
        #self.h, self.m, self.s = ["10", "37", "49"]

        self.title("Bin Clock")
        self.resizable(0, 0)
        #self["bg"] = "#FFFFFF"
        
        self.black = "#D9D9D9"
        self.blue = "#7289DA"

        frames_names = ["Hour", "Minute", "Second"]
        self.frames_list = []

        #Frames placed
        for name in range(3):
            self.frames_list.append(
                LabelFrame(self, text=frames_names[name]))
            
            self.frames_list[name].config(padx=5, pady=5, font=("Verdana",9))
            self.frames_list[name].grid(row=0, column=name, padx=5, pady=5)

        self.hour_lamps = []
        self.minute_lamps = []
        self.second_lamps = []

        self.lamps_list = [
            self.hour_lamps,
            self.minute_lamps,
            self.second_lamps
            ]
        
        for i in range(3):
            self.place_lamps(self.lamps_list[i], self.frames_list[i])

        self.main()
        
    def place_lamps(self, l, f):
        index = 0
        for y in range(4):
            for lampx in range(2):
                l.append(Label(f))

                l[index].config(
                    bg=self.black, width=2,
                    height=1, relief=FLAT)

                l[index].grid(
                    row=y, column=lampx,
                    padx=1, pady=1)

                index += 1
                
    def main(self):
        self.update_hour()
        self.update_minute()
        self.update_second()

    #It has to be made better
    def update_hour(self):
        h = self.get_time()[0]
        self.place_colors(self.hour_lamps, h)
        self.frames_list[0].after(
            1000, self.update_hour)

    def update_minute(self):
        m = self.get_time()[1]
        self.place_colors(self.minute_lamps, m)
        self.frames_list[1].after(
            1000, self.update_minute)

    def update_second(self):
        s = self.get_time()[2]
        self.place_colors(self.second_lamps, s)
        self.frames_list[2].after(
            1000, self.update_second)
            
    def place_colors(self, lamp_list, time):
        binary_numbers  = self.dec_to_bin(time)

        i = 0
        for b in binary_numbers:
            if b == "1":
                lamp_list[i]["bg"] = self.blue
            else:
                lamp_list[i]["bg"] = self.black
            i += 1
    
    def dec_to_bin(self, num):
        s1, s2 = [
            bin(int(num[i]))[2:] for i in range(2)
            ]
        
        if len(s1) < 4:
            zero = 4 - len(s1)
            s1 = (zero * "0") + s1

        if len(s2) < 4:
            zero = 4 - len(s2)
            s2 = (zero * "0") + s2

        unified = ""
        
        for i in list(zip(s1, s2)):
            unified += str(i[0]) + str(i[1])

        return unified

    def get_time(self):
        time = datetime.now().strftime('%H:%M:%S')
        return time.split(":")
        
if __name__ == "__main__":
    root = Template()
    root.mainloop()

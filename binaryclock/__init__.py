from .clock import Clock


#          H-H    M-M    S-S
#         +-+-+  +-+-+  +-+-+
#  2^3=8  |1|2|  |1|2|  |1|2|
#  2^2=4  |3|4|  |3|4|  |3|4|
#  2^1=2  |5|6|  |5|6|  |5|6|
#  2^0=1  |7|8|  |7|8|  |7|8|
#         +-+-+  +-+-+  +-+-+


def launch():
    root = Clock()
    root.title("BinaryClock")
    root.resizable(0, 0)
    root.mainloop()

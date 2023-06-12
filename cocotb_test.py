import cocotb 
from cocotb.clock import Clock
from cocotb.triggers import Edge, First, NextTimeStep
import tkinter as tk


@cocotb.test()
async def cocotb_test(dut):
    c = Clock(dut.clk, 100, 'ns')
    await cocotb.start(c.start())
    await reset(dut)
    digit0 = digit1 = digit2 = digit3 = 0xFE
    change = True
    root = tk.Tk()
    root.title("7 segment display")
    screen = tk.Canvas(root)
    screen.grid()
    dig0 = Digit(screen, 10, 10) 
    dig1 = Digit(screen, 40, 10) 
    dig2 = Digit(screen, 70, 10) 
    dig3 = Digit(screen, 100, 10)
    while True:
        digit_num, digit = await read_seg(dut)
        if digit_num == 0 and digit0 != digit: 
            digit0 = digit
            change = True
        elif digit_num == 1 and digit1 != digit:
            digit1 = digit
            change = True
        elif digit_num == 2 and digit2 != digit:
            digit2 = digit
            change = True
        elif digit_num == 3 and digit3 != digit:
            digit3 = digit
            change = True
        if change:
            num =int_to_seg(digit0) + int_to_seg(digit1)*10 + int_to_seg(digit2)*100 + int_to_seg(digit3)*1000
            dig0.show(int_to_seg(digit0))
            dig1.show(int_to_seg(digit1))
            dig2.show(int_to_seg(digit2))
            dig3.show(int_to_seg(digit3))
            cocotb.log.debug(f"digit num = {num}")
            cocotb.log.debug(f"clock =  {int_to_seg(digit0)} {int_to_seg(digit1)} {int_to_seg(digit2)} {int_to_seg(digit3)}")
            change = False
        if int_to_seg(digit3) == 9:
            break
        root.update()



async def reset (dut):
    dut.rst.value = 1
    await cocotb.triggers.Timer(1000, 'ns')
    dut.rst.value = 0


async def read_seg(dut):
    # wait for any change at digit_en
    await Edge(dut.digit_en)
    await NextTimeStep() # make sure no race happened 
    digit_en = dut.digit_en.value.integer
    digit = dut.seven_seg.value.integer
    cocotb.log.debug(f"digit_en = {hex(digit_en)} digit = {hex(digit)}")
    if (digit_en == 0xE):
        digit_num = 0
    elif (digit_en == 0xD):
        digit_num = 1
    elif (digit_en == 0xB):
        digit_num = 2
    elif (digit_en == 0x7):
        digit_num = 3
    else: 
        cocotb.log.error(f"Invalid digit_en: {digit_en}")

    return digit_num, digit

def int_to_seg(digit):
    return {
        0xFE: 0,
        0xB0: 1,
        0xED: 2,
        0xF9: 3,
        0xB3: 4,
        0xDB: 5,
        0xDF: 6,
        0xF0: 7,
        0xFF: 8,
        0xFB: 9,
    }[digit]    
    
class Digit:
    def __init__(self, canvas, x=10, y=10, length=20, width=4):
        self.canvas = canvas
        l = length
        self.segs = []
        offsets = offsets = (
            (0, 0, 1, 0),  # top
            (1, 0, 1, 1),  # upper right
            (1, 1, 1, 2),  # lower right
            (0, 2, 1, 2),  # bottom
            (0, 1, 0, 2),  # lower left
            (0, 0, 0, 1),  # upper left
            (0, 1, 1, 1),  # middle
        )
        self.digits = (
            (1, 1, 1, 1, 1, 1, 0),  # 0
            (0, 1, 1, 0, 0, 0, 0),  # 1
            (1, 1, 0, 1, 1, 0, 1),  # 2
            (1, 1, 1, 1, 0, 0, 1),  # 3
            (0, 1, 1, 0, 0, 1, 1),  # 4
            (1, 0, 1, 1, 0, 1, 1),  # 5
            (1, 0, 1, 1, 1, 1, 1),  # 6
            (1, 1, 1, 0, 0, 0, 0),  # 7
            (1, 1, 1, 1, 1, 1, 1),  # 8
            (1, 1, 1, 1, 0, 1, 1),  # 9
        )
        for x0, y0, x1, y1 in offsets:
            self.segs.append(canvas.create_line(
                x + x0*l, y + y0*l, x + x1*l, y + y1*l,
                width=width, state = 'hidden'))
    def show(self, num):
        for iid, on in zip(self.segs, self.digits[num]):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')
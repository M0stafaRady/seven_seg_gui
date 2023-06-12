import cocotb 
from cocotb.clock import Clock
from cocotb.triggers import Edge, First, NextTimeStep


@cocotb.test()
async def cocotb_test(dut):
    c = Clock(dut.clk, 50, 'ns')
    await cocotb.start(c.start())
    await reset(dut)
    digit0 = digit1 = digit2 = digit3 = 0xFE
    change = True
    for i in range(10000):
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
            cocotb.log.info(f"digit num = {digit_num}")
            cocotb.log.info(f"clock =  {int_to_seg(digit0)} {int_to_seg(digit1)} {int_to_seg(digit2)} {int_to_seg(digit3)}")
            change = False



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
    
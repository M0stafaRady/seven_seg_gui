

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/timer.v $(PWD)/timer_tb.v 

TOPLEVEL := timer_tb
MODULE   := cocotb_test

include $(shell cocotb-config --makefiles)/Makefile.sim
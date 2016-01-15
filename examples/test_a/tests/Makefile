TOPLEVEL := axi
#TOPLEVEL := test
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
COCOTB=$(PWD)/../../..

WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)

export PYTHONPATH

#VERILOG_SOURCES = $(WPWD)/../hdl/adder.v
VERILOG_SOURCES = $(WPWD)/../hdl/axi.v
#VERILOG_SOURCES = $(WPWD)/../hdl/test.v
GPI_IMPL := vpi

#SRC_BASE = ../../axi_pm/rtl
#INCDIRS += +incdir+$(SRC_BASE) 
#VERILOG_SOURCES =	$(SRC_BASE)/axi_port_define.v \
#					$(SRC_BASE)/AXI_PM_CSR.v \
#					$(SRC_BASE)/axi_pm.v \
#					$(SRC_BASE)/axi_read_wrapper.v \
#					$(SRC_BASE)/ivsn_mon.v \
#					$(SRC_BASE)/max.v \
#					$(SRC_BASE)/min.v \
#					$(SRC_BASE)/pm_mon.v \
#					$(SRC_BASE)/pm_sub.v \
#					$(SRC_BASE)/rd_cnt.v \
#					$(SRC_BASE)/reset_sync.v \
#					$(SRC_BASE)/sync.v \
#					$(SRC_BASE)/tick_cnt.v \
#					$(SRC_BASE)/wr_cnt.v 

#FSDB_DUMP = -ucli -i $(PWD)/fsdb.dump
#INCDIRS += +incdir+$(SRC_BASE) 

export TOPLEVEL_LANG

MODULE ?= test_axi

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

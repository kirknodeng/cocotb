# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.result import TestFailure
from cocotb.drivers import BusDriver 
from cocotb.drivers.amba import AXI4LiteMaster
import random

class AXI4_IF_TB(object):
	def __init__(self, dut, debug=True):
		self.dut = dut
		self.input = AXI4LiteMaster(dut, "i", dut.i_ACLK)
		self.dut.log.info("test_drvTB init")

	@cocotb.coroutine
	def reset(self, duration=10000):
		self.dut.log.debug("Resetting DUT")
		self.dut.i_ARESETn <= 0

		yield Timer(duration)
		yield RisingEdge(self.dut.i_ACLK)
		self.dut.i_ARESETn <= 1
		self.dut.log.debug("Out of reset")


@cocotb.test()
#@cocotb.coroutine
def run_test(dut):

	cocotb.fork(clock_gen(dut.i_ACLK))

	yield RisingEdge(dut.i_ACLK)
	tb = AXI4_IF_TB(dut)

	yield tb.reset()

	for i in range(1,5):
		yield tb.input.write(i,55+i)

	yield RisingEdge(dut.i_ACLK)
	dut.log.info("DUT")

@cocotb.coroutine
def clock_gen(signal):
	while True:
		signal <= 0
		yield Timer(5000)
		signal <= 1
		yield Timer(5000)



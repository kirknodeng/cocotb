# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.result import TestFailure
from cocotb.drivers import BusDriver 
from adder_model import adder_model
import random
from test_drv import test_drv


class test_drvTB(object):
	def __init__(self, dut, debug=True):
		self.dut = dut
		self.test_in = test_drv(dut, "", dut.clock )
		#self.dut.log.info("test_drvTB init")

	@cocotb.coroutine
	def reset(self, duration=10000):
		#self.dut.log.debug("Resetting DUT")
		self.dut.resetn <= 0

		yield Timer(duration)
		yield RisingEdge(self.dut.clock)
		self.dut.resetn <= 1
		#self.dut.log.debug("Out of reset")


@cocotb.test()
#@cocotb.coroutine
def run_test(dut):

	cocotb.fork(clock_gen(dut.clock))

	yield RisingEdge(dut.clock)
	tb = test_drvTB(dut)

	yield tb.reset()

	for i in range(5):
		yield tb.test_in.write(i,3,dut.clock)
		yield Timer(100)

	yield RisingEdge(dut.clock)
	#for i in range(5):
	#dut.log.info("DUT")

@cocotb.coroutine
def clock_gen(signal):
	while True:
		signal <= 0
		yield Timer(5000)
		signal <= 1
		yield Timer(5000)



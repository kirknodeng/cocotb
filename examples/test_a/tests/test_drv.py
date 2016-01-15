import random

import cocotb
from cocotb.drivers import BusDriver 
from cocotb.triggers import RisingEdge, ReadOnly, Event

class test_drv(BusDriver):
    _signals = ["A", "B", "X"]
    _optional_signals= []

    def __init__(self, entity, name, clock):
        BusDriver.__init__(self, entity, name, clock)
        self.bus.A.setimmediatevalue(5)
        self.bus.B.setimmediatevalue(5)
        self.log.debug("Test DrvM created")
        self.busy_event = Event("%s_busy" % name)
        self.busy = False

    @cocotb.coroutine
    def _acquire_lock(self):
        if self.busy:
            yield self.busy_event.wait()
        self.busy_event.clear()
        self.busy = True

    def _release_lock(self):
        self.busy = False
        self.busy_event.set()


    @cocotb.coroutine
    def write(self, value_a, value_b, sync=True):
        """
        """
        yield self._acquire_lock()

        if sync:
            yield RisingEdge(self.clock)
        self.bus.A <= value_a
        self.bus.B <= value_b

        self._release_lock()

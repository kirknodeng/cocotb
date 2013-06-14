#!/bin/env python

''' Copyright (c) 2013 Potential Ventures Ltd
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Potential Ventures Ltd nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL POTENTIAL VENTURES LTD BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. '''

"""

    Class defining the standard interface for a monitor within a testbench

    The monitor is responsible for watching the pins of the DUT and recreating the
    transactions
"""

import logging
import math

import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Edge, Event, RisingEdge
from cocotb.binary import BinaryValue
from cocotb.bus import Bus
from cocotb.utils import hexdump

class Monitor(object):


    def __init__(self, callback=None, event=None):
        """
        Constructor for a monitor instance

        callback will be called with each recovered transaction as the argument

        If the callback isn't used, received transactions will be placed on a queue and the
        event used to notify any consumers.
        """
        self._event = event
        self._recvQ = []
        self._callbacks = []

        # Subclasses may already set up logging
        if not hasattr(self, "log"):
            self.log = logging.getLogger("cocotb.monitor.%s" % (self.__class__.__name__))

        if callback is not None:
            self.add_callback(callback)

        # Create an independent coroutine which can receive stuff
        self._thread = cocotb.scheduler.add(self._monitor_recv())

    def kill(self):
        if self._thread:
            self._thread.kill()
            self._thread = None

    def __len__(self):
        return len(self._recvQ)

    def add_callback(self, callback):
        self.log.debug("Adding callback of function %s to monitor" % (callback.__name__))
        self._callbacks.append(callback)

    @coroutine
    def _monitor_recv(self):
        """
        actual impementation of the receiver

        subclasses should override this method to implement the actual receive routine and
        call self._recv() with the recovered transaction
        """
        raise NotImplementedError("Attempt to use base monitor class without providing a _monitor_recv method")


    def _recv(self, transaction):
        """Common handling of a received transaction."""
        # either callback based consumer
        for callback in self._callbacks:
            callback(transaction)

        # Or queued with a notification
        if not self._callbacks:
            self._recvQ.append(transaction)

        if self._event is not None:
            self._event.set()


class AvalonST(Monitor):
    _signals = ["valid", "data"]



class AvalonSTPkts(Monitor):
    """
    Packetised AvalonST bus
    """
    _signals = AvalonST._signals + ["startofpacket", "endofpacket", "ready", "empty", "error"]

    def __init__(self, entity, name, clock, callback=None, event=None):
        self.entity = entity
        self.name = name
        self.clock = clock
        self.bus = Bus(self.entity, self.name, self._signals)
        self.log = logging.getLogger("cocotb.%s.%s" % (self.entity.name, self.name))

        Monitor.__init__(self, callback=callback, event=event)

    @coroutine
    def _monitor_recv(self):
        """Watch the pins and reconstruct transactions"""

        # Avoid spurious object creation by recycling
        clkedge = RisingEdge(self.clock)
        pkt = ""

        while True:
            yield clkedge

            if self.bus.valid.value and self.bus.startofpacket.value:
                vec = self.bus.data.value
                self.bus.data.log.info("%s %s" % (vec.binstr, repr(vec.buff)))
                pkt += vec.buff
                while True:
                    yield clkedge
                    if self.bus.valid.value:
                        vec = self.bus.data.value
                        self.bus.data.log.debug("%s %s" % (vec.binstr, repr(vec.buff)))
                        pkt += vec.buff
                        if self.bus.endofpacket.value:
                            self.log.info("Recieved a packet of %d bytes" % len(pkt))
                            self.log.debug(hexdump(str((pkt))))
                            self._recv(pkt)
                            pkt = ""
                            break



class SFStreaming(Monitor):
    """This is the Solarflare Streaming bus as defined by the FDK.

    Expect to see a 72-bit bus (bottom 64 bits data, top 8 bits are ECC)

    TODO:
        Metaword / channel bits
        ECC checking
    """
    _signals = AvalonST._signals + ["startofpacket", "endofpacket", "ready", "empty", "channel", "error"]

    def __init__(self, entity, name, clock, callback=None, event=None):
        self.entity = entity
        self.name = name
        self.clock = clock
        self.bus = Bus(self.entity, self.name, self._signals)
        self.log = logging.getLogger("cocotb.%s.%s" % (self.entity.name, self.name))

        Monitor.__init__(self, callback=callback, event=event)

    @coroutine
    def _monitor_recv(self):
        """Watch the pins and reconstruct transactions"""

        # Avoid spurious object creation by recycling
        clkedge = RisingEdge(self.clock)
        pkt = ""

        while True:
            yield clkedge

            if self.bus.valid.value and self.bus.startofpacket.value:
                vec = self.bus.data.value
                self.bus.data.log.info("%s %s" % (vec.binstr, repr(vec.buff)))
                pkt += vec.buff
                while True:
                    yield clkedge
                    if self.bus.valid.value:
                        vec = self.bus.data.value
                        self.bus.data.log.info("%s %s" % (vec.binstr, repr(vec.buff)))
                        pkt += vec.buff
                        if self.bus.endofpacket.value:
                            self.log.warning("Recieved a packet!!")
                            self.log.info(repr(pkt))
                            self._recv(pkt)
                            pkt = ""
                            break
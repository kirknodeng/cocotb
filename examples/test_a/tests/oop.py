class BusDriver(object):
    def __init__(self, entity, name, clock):
		print "initial"
		print entity
		print name
		print clock

class test_oop(BusDriver):
    _signals = ["A", "B", "X"]

    def __init__(self, *args, **kwargs):
        BusDriver.__init__(self, *args, **kwargs)


class test_prog(object):
	def __init__(self, *args, **kwargs):
		self.test1 = test_oop(*args, **kwargs)


tb = test_prog("dut", "name", "clock")



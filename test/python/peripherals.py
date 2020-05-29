#a Copyright
#  
#  This file 'bfm.py' copyright Gavin J Stark 2017-2020
#  
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, version 2.0.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#  for more details.

#a Imports
from regress.apb.structs import t_apb_request, t_apb_response
from regress.apb.bfm     import ApbMaster
from cdl.sim     import ThExecFile
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase
from regress.apb import target_timer, target_gpio

from cdl.utils   import csr
class ApbAddressMap(csr.Map):
    _width=32
    _select=0
    _address=0
    _shift=2
    _address_size=0
    _map=[csr.MapMap(offset=0, name="timer", map=target_timer.TimerAddressMap),
         ]
    pass
#c apb_timer_thef
class apb_timer_thef(ThExecFile):
    th_name = "APB timer test harness"
    def run(self) -> None:
        self.apb = ApbMaster(self, "signal__apb_request",  "signal__apb_response")
        self.apb_map = ApbAddressMap()
        self.timer_map  = self.apb_map.timer # This is an ApbAddressMap()
        self.timer      = self.apb.reg(self.timer_map.timer)
        self.timer_cmp0 = self.apb.reg(self.timer_map.comparator0)
        self.bfm_wait(25)
        self.timer_cmp0.write(0xdeedbeef)
        print("Read %08x"%self.timer_cmp0.read())
        timers = []
        for i in range(10):
            timers.append(self.timer.read())
            pass
        for i in timers:print("%08x"%i)
        apb_write_in_cycles = (timers[-1]-timers[-2])
        self.timer_cmp0.write(timers[-1]+5*apb_write_in_cycles)
        comparators = []
        for i in range(10):
            comparators.append( (self.timer_cmp0.read(),self.timer.read()) )
            pass
        for (i,j) in comparators:print("%08x %08x"%(i,j))
        self.passtest("Test succeeded")
        pass

#c ApbTimerHardware
class ApbTimerHardware(HardwareThDut):
    clock_desc = [("clk",(0,1,1))]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "apb_target_timer"
    dut_outputs = {"apb_response":t_apb_response,
                   "timer_equalled":3
    }
    dut_inputs  = {"apb_request":t_apb_request,
    }
    th_options = {"signal_object_prefix":"signal__",
                 }
    th_exec_file_object_fn = apb_timer_thef
    pass

#c TestApbTimer
class TestApbTimer(TestCase):
    hw = ApbTimerHardware
    def test_1(self)->None:
        self.run_test(hw_args={"verbosity":0}, run_time=5000)
        pass
    pass


#a Copyright
#  
#  This file 'test_timer.py' copyright Gavin J Stark 2017-2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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
    pass

#c TestApbTimer
class TestApbTimer(TestCase):
    hw = ApbTimerHardware
    _tests = {"simple": (apb_timer_thef, 5*1000, {"verbosity":0}),
              }
    pass

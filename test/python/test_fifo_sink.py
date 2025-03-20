#a Imports
from regress.utils import t_dprintf_req_4, t_dprintf_byte, Dprintf, DprintfBus, FifoStatus
from regress.apb.structs import t_apb_request, t_apb_response
from regress.apb.bfm     import ApbMaster
from cdl.sim     import ThExecFile
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase
from regress.apb import target_timer, target_gpio
from regress.apb import FifoSinkAddressMap

from cdl.utils   import csr

#c ApbAddressMap
class ApbAddressMap(csr.Map):
    _width=32
    _select=0
    _address=0
    _shift=0
    _address_size=0
    _map=[csr.MapMap(offset=0, name="fifo_sink", map=FifoSinkAddressMap),
         ]
    pass

#a TestBase
#c TestBase
class TestBase(ThExecFile):
    th_name = "APB timer test harness"
    #f drive_dprintf_req
    def drive_dprintf_req(self, d):
        self.dprintf.drive(d)
        self.bfm_wait(1)
        while not self.dprintf.is_acked():
            self.bfm_wait(1)
            pass
        self.dprintf.invalid()
        pass

    #f run
    def run(self) -> None:

        self.apb = ApbMaster(self, "apb_request",  "apb_response")
        self.apb_map = ApbAddressMap()
        self.fifo_sink_map    = self.apb_map.fifo_sink
        self.dprintf = DprintfBus(self, "dprintf_req", "dprintf_ack", n=4)

        self.config_status = self.apb.reg(self.fifo_sink_map.config_status)
        self.fifo_status   = self.apb.reg(self.fifo_sink_map.fifo_status)
        self.fifo_data     = self.apb.reg(self.fifo_sink_map.fifo_data)
        self.bfm_wait(10)

        self.config_status.write(0xff) # 8 words per entr
        cs = self.config_status.read()
        self.compare_expected("Cs with words-per-entry written",cs,7)

        self.config_status.write(0x1) # 2 words per entr
        cs = self.config_status.read()
        self.compare_expected("Cs with words-per-entry written",cs,1)

        self.config_status.write(0x2) # 3 words per entry
        cs = self.config_status.read()
        self.compare_expected("Cs with words-per-entry written",cs,2)

        self.bfm_wait(10)

        fs = self.fifo_status.read()
        self.compare_expected("Fifo status empty",fs,FifoStatus(515,0).as_csr32())

        data = [ Dprintf(0x0, b"abcdefghijklmnop"),
         ]
        for d in data:
            self.drive_dprintf_req(d)
            pass

        self.bfm_wait(20)

        fs = self.fifo_status.read()
        self.compare_expected("Fifo status empty",fs,FifoStatus(515,1).as_csr32())

        x = self.fifo_data.read()
        self.compare_expected("data",x,0x65666768)

        fs = self.fifo_status.read()
        self.compare_expected("Fifo status empty",fs,FifoStatus(515,0).as_csr32())

        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry set",cs,16)

        x = self.fifo_data.read()
        self.compare_expected("data",x,0x61626364)
        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry set",cs,16)

        x = self.fifo_data.read()
        self.compare_expected("data",x,0x6d6e6f78)
        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry clear",cs,0)

        # Underflow
        x = self.fifo_data.read()
        self.compare_expected("data",x,0)
        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have empty and sticky empty set",cs,0x60)
        x = self.fifo_data.read()
        x = self.fifo_data.read()

        data = [ Dprintf(0x0, b"abcdefghijklmnop"),
                 Dprintf(0x0, b"abcdefghijklmnop"),
                 Dprintf(0x0, b"abcdefghijklmnop"),
                ]
        for d in data:
            self.drive_dprintf_req(d)
            pass

        self.bfm_wait(20)

        fs = self.fifo_status.read()
        self.compare_expected("Fifo status 3 entries",fs,FifoStatus(515,3).as_csr32())

        x = self.fifo_data.read()
        self.compare_expected("data",x,0x65666768)

        fs = self.fifo_status.read()
        self.compare_expected("Fifo status 2 entries",fs,FifoStatus(515,2).as_csr32())

        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry set + sticky",cs,0x50)

        x = self.fifo_data.read()
        self.compare_expected("data",x,0x61626364)
        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry set",cs,0x50)

        x = self.fifo_data.read()
        self.compare_expected("data",x,0x6d6e6f78)
        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry clear",cs,0x40)

        # Underflow
        x = self.fifo_data.read()
        self.compare_expected("data",x,0x65666768)
        cs = self.config_status.read()&0xf0
        self.compare_expected("Cs should have mid-entry set and sticky empty set",cs,0x50)

        self.passtest("Test succeeded")
        pass

#c ApbTest0
class ApbTest0(TestBase):
    pass

#c ApbHardware
class ApbHardware(HardwareThDut):
    clock_desc = [("clk",(0,1,1))]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "tb_apb_fifo_sink"
    dut_inputs  = {"apb_request":t_apb_request,
                   "dprintf_req":t_dprintf_req_4,
    }
    dut_outputs = {"apb_response":t_apb_response,
                   "dprintf_ack":1,
    }
    pass

#c TestApbFifoSink
class TestApbFifoSink(TestCase):
    hw = ApbHardware
    _tests = {"0": (ApbTest0, 5*1000, {"verbosity":0}),
              "smoke": (ApbTest0, 5*1000, {"verbosity":0}),
              }
    pass


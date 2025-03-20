#a Imports
from regress.apb.structs import t_apb_request, t_apb_response
from regress.apb.bfm     import ApbMaster
from cdl.sim     import ThExecFile
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase
from regress.apb import SramInterfaceAddressMap

from cdl.utils   import csr

#c ApbAddressMap
class ApbAddressMap(csr.Map):
    _width=32
    _select=0
    _address=0
    _shift=0
    _address_size=0
    _map=[csr.MapMap(offset=0, name="sram_interface", map=SramInterfaceAddressMap),
         ]
    pass

#a TestBase
#c TestBase
class TestBase(ThExecFile):
    th_name = "APB Sram Interface harness"
    inter_delay = 1 # Minimum 1
    #f run
    def run(self) -> None:

        self.apb = ApbMaster(self, "apb_request",  "apb_response")
        self.apb_map = ApbAddressMap()
        self.sram_map    = self.apb_map.sram_interface

        self.address = self.apb.reg(self.sram_map.address)
        self.control = self.apb.reg(self.sram_map.control)
        self.data = self.apb.reg(self.sram_map.data)
        self.data_inc = self.apb.reg(self.sram_map.data_inc)
        self.bfm_wait(10)

        for d in [0x12345678, 0xdeadbeef, 0xf00dcafe]:
            self.control.write(d)
            c = self.control.read()
            self.compare_expected("Control wrote",c,d)
            self.compare_expected("Control out",c,self.sram_ctrl.value())
            self.bfm_wait(self.inter_delay)
            pass

        for i in range(10):
            d = (0xdeadbeef*i+0xf00dcafe) & 0xffffffff
            self.address.write(i)
            self.data.write(d)
            self.bfm_wait(self.inter_delay)
            pass
        
        for i in range(10):
            d = (0xdeadbeef*i+0xf00dcafe) & 0xffffffff
            self.address.write(i)
            x = self.data.read()
            self.compare_expected("Data read back for %d"%i,x,d)
            self.bfm_wait(self.inter_delay)
            pass
        
        self.address.write(0)
        for i in range(10):
            d = (0xdeadbeef*i+0xf00dcafe) & 0xffffffff
            x = self.data_inc.read()
            self.compare_expected("Data read back for %d"%i,x,d)
            self.bfm_wait(self.inter_delay)
            pass
        
        self.passtest("Test succeeded")
        pass

#c ApbTest0
class ApbTest0(TestBase):
    inter_delay = 1
    pass

#c ApbTest1
class ApbTest1(TestBase):
    inter_delay = 3
    pass

#c ApbHardware
class ApbHardware(HardwareThDut):
    clock_desc = [("clk",(0,1,1))]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "tb_apb_sram_interface"
    dut_inputs  = {"apb_request":t_apb_request,
    }
    dut_outputs = {"apb_response":t_apb_response,
                   "sram_ctrl":32,
    }
    pass

#c TestApbSramInterface
class TestApbSramInterface(TestCase):
    hw = ApbHardware
    _tests = {"0": (ApbTest0, 5*1000, {"verbosity":0}),
              "1": (ApbTest1, 5*1000, {"verbosity":0}),
              "smoke": (ApbTest0, 5*1000, {"verbosity":0}),
              }
    pass


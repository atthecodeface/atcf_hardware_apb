#a Copyright
#  
#  This file 'test_processor.py' copyright Gavin J Stark 2017-2020
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
import tempfile
from regress.apb.structs import t_apb_processor_request, t_apb_processor_response
from regress.apb.rom     import Rom
from cdl.sim     import ThExecFile
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase
from cdl.utils.memory import Memory

from cdl.utils   import csr
from regress.apb import target_timer, target_gpio, target_sram_interface

#a Address map
#c ApbAddressMap
class ApbAddressMap(csr.Map):
    _width=32
    _select=0
    _address=0
    _shift=0
    _address_size=0
    _map=[csr.MapMap(offset=0,          name="timer", map=target_timer.TimerAddressMap),
          csr.MapMap(offset=0x10000000, name="gpio",  map=target_gpio.GpioAddressMap),
          csr.MapMap(offset=0x20000000, name="sram",  map=target_sram_interface.SramInterfaceAddressMap),
         ]
    pass
#c ProcessorTestBase
class ProcessorTestBase(ThExecFile):
    apb = ApbAddressMap()
    th_name = "APB processor test harness"
    #v program
    defines = {"nothing":"value"}
    program = {}
    program["code"] = []
    program["code"] += [
        (Rom.op_finish(),["prog_finish:"]),
        ]
    program["code"] += [
        (Rom.op_set("address",apb.gpio.output.Address()),["prog_gpio_rw:"]),
        (Rom.op_req("write_arg",0xffffffff),),
        (Rom.op_req("read",0),),
        (Rom.op_branch("beq",0),["fail"]),
        (Rom.op_alu("add",1),),
        (Rom.op_branch("bne",0),["fail"]),
        (Rom.op_finish(),),
        ]
    program["code"] += [
        (Rom.op_set("address",apb.timer.timer.Address()),["prog_timer_comparator:"]),
        (Rom.op_req("read",0),),
        (Rom.op_alu("add",40),),
        (Rom.op_set("address",apb.timer.comparator0.Address()),),
        (Rom.op_req("write_acc",0),),
        (Rom.op_req("read",0),["read_loop:"]),
        (Rom.op_alu("and",0x80000000),),
        (Rom.op_branch("beq",0),["read_loop"]),
        ]
    program["code"] += [
        (Rom.op_finish(),),
        ]
    program["code"] += [
        (Rom.op_branch("branch",0),["fail:","fail"]),
        ]
    program["code"] += [
        (Rom.op_set("address",apb.sram.control.Address()),["prog_sram_gpio:"]),
        (Rom.op_req("write_arg",0x123),),
        (Rom.op_set("address",apb.gpio.input_status.Address()),),
        (Rom.op_req("read",0),),
        (Rom.op_alu("and",0xfff8),),
        (Rom.op_alu("xor",0x123<<3),),
        (Rom.op_branch("bne",0),["fail"]),
        (Rom.op_finish(),),
        ]
    program["code"] += [
        (Rom.op_set("address",apb.sram.address.Address()),["prog_sram:"]),
        (Rom.op_req("write_arg",0),),
        (Rom.op_set("address",apb.sram.data_inc.Address()),),
        (Rom.op_set("accumulator",0x1234),),
        (Rom.op_set("repeat",20),),
        (Rom.op_req("write_acc",0),["sram_write_loop:"]),
        (Rom.op_alu("add",0x3),),
        (Rom.op_branch("loop",0),["sram_write_loop"]),
        (Rom.op_set("address",apb.sram.address.Address()),),
        (Rom.op_req("write_arg",0),),
        (Rom.op_set("address",apb.sram.data_inc.Address()),),
        (Rom.op_set("repeat",20),),
        (Rom.op_req("read",0),["sram_read_loop:"]),
        (Rom.op_branch("loop",0),["sram_read_loop"]),
        (Rom.op_alu("xor",0x1234 + 20*3),),
        (Rom.op_branch("bne",0),["fail"]),
        (Rom.op_finish(),),
        ]
    programs_to_run = [ "prog_timer_comparator" ]
    #f invoke_program
    def invoke_program(self, address):
        self.compare_expected("acknowledge should start low",
                              self.apb_processor_response__acknowledge.value(), 0 )
        self.apb_processor_request__address.drive(address)
        self.apb_processor_request__valid.drive(1)
        self.bfm_wait(1)
        self.apb_processor_response__acknowledge.wait_for_value(1)
        self.apb_processor_request__valid.drive(0)
        self.bfm_wait(1)
        self.compare_expected("acknowledge should be cleared after valid goes away",
                              self.apb_processor_response__acknowledge.value(), 0 )
        self.compare_expected("busy should become set",
                              self.apb_processor_response__rom_busy.value(), 1 )
        self.apb_processor_response__rom_busy.wait_for_value(0)
        pass
    #f run_init
    def run__init(self) -> None:
        self.bfm_wait(2)
        self.tempfile = self.hardware.tempfile
        self.sim_msg = self.sim_message()
        compiled_program = Rom.compile_program(self.program)
        self.memory = Memory(bit_width=40)
        compiled_program.add_to_memory(self.memory, bytes_per_word=5)
        self.tempfile.seek(0)
        self.tempfile.truncate(0)
        self.memory.write_mif(self.tempfile)
        self.tempfile.flush()
        # self.tempfile.seek(0)
        # for l in self.tempfile:print(l)
        self.sim_msg.send_value("dut.apb_rom",2,0) # Force reset the SRAM to load its file
        pass
    def run(self) -> None:
        self.bfm_wait(10)
        for l in self.programs_to_run:
            a = self.memory.resolve_label(l+":")
            self.verbose.info("Start program at label %s address %d"%(l,a))
            self.invoke_program(a)
            pass
        self.passtest("Test succeeded")
        pass

#c ProcessorTest0
class ProcessorTest0(ProcessorTestBase):
    programs_to_run = [ "prog_finish",
                        "prog_timer_comparator",
                        "prog_gpio_rw",
                        "prog_sram_gpio",
                        "prog_sram",
    ]
    pass

#c ApbProcessorHardware
class ApbProcessorHardware(HardwareThDut):
    clock_desc = [("clk",(0,1,1))]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "tb_apb_processor"
    dut_inputs  = {"apb_processor_request":t_apb_processor_request,
    }
    dut_outputs = {"apb_processor_response":t_apb_processor_response,
                   "timer_equalled":3
    }
    loggers = { # "apb":{"modules":"dut dut.apb_log", "verbose":1},
                # "apb":{"modules":"dut.apb_log", "verbose":1},
                }
    def __init__(self, **kwargs):
        self.tempfile = tempfile.NamedTemporaryFile(mode='w+')
        self.hw_forces = {"apb_rom.filename":self.tempfile.name}
        super(ApbProcessorHardware,self).__init__(**kwargs)
        pass
    pass

#c TestApbProcessor
class TestApbProcessor(TestCase):
    hw = ApbProcessorHardware
    _tests = {"smoke": (ProcessorTest0, 100*1000, {"verbosity":0}),
              }
    pass


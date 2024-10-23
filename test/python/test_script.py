#a Copyright
#  
#  This file 'test_script_master.py' copyright Gavin J Stark 2017-2020
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
from random import Random
from regress.apb.structs import t_apb_script_master_request, t_apb_script_master_op
from regress.apb.structs import t_apb_script_master_response, t_apb_script_master_resp_type
from regress.apb import Script
from cdl.sim     import ThExecFile
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase

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
#c ScriptMasterTestBase
class ScriptMasterTestBase(ThExecFile):
    apb = ApbAddressMap()
    th_name = "APB script_master test harness"
    random_seed = "some tx random seed"
    #v program
    defines = {"nothing":"value"}
    scripts = {}
    scripts["none"] = ([],"ok",[])
    scripts["gpio_rw"] = ([
        Script.op_set("addr1",apb.gpio.output.Address()>>8),
        Script.op_set("addr2",apb.gpio.output.Address()>>16),
        Script.op_set("addr3",apb.gpio.output.Address()>>24),
        Script.op_write(apb.gpio.output.Address(),32,[0xffffffff]),
        Script.op_read(apb.gpio.output.Address(),32),
        ],"ok",[(0xffffffff,0xffffffff),])
    scripts["timer_comparator"] = ([
        Script.op_set("addr1",apb.timer.timer.Address()>>8),
        Script.op_set("addr2",apb.timer.timer.Address()>>16),
        Script.op_set("addr3",apb.timer.timer.Address()>>24),
        Script.op_set("poll_delay",14),
        Script.op_write(apb.timer.comparator0.Address(),16,[0x100]),
        Script.op_poll_set(apb.timer.comparator0.Address(),31),
        Script.op_read(apb.timer.comparator0.Address(),32),
        ],"ok",[(0xffffff00,0x00000100)])
    scripts["sram_gpio"] = ([
        Script.op_set("addr1",apb.sram.control.Address()>>8),
        Script.op_set("addr2",apb.sram.control.Address()>>16),
        Script.op_set("addr3",apb.sram.control.Address()>>24),
        Script.op_write(apb.sram.control.Address(),32,[0x123]),
        Script.op_set("addr1",apb.gpio.input_status.Address()>>8),
        Script.op_set("addr2",apb.gpio.input_status.Address()>>16),
        Script.op_set("addr3",apb.gpio.input_status.Address()>>24),
        Script.op_read(apb.gpio.input_status.Address(),16),
        ],"ok",[(0xfff8,0x123<<3)])
    scripts["sram"] = ([
        Script.op_set("addr1",apb.sram.address.Address()>>8),
        Script.op_set("addr2",apb.sram.address.Address()>>16),
        Script.op_set("addr3",apb.sram.address.Address()>>24),
        Script.op_write(apb.sram.address.Address(),32,[0]),
        Script.op_write(apb.sram.data_inc.Address(),32,[0x1234567, 0x2345678]),
        Script.op_write(apb.sram.address.Address(),32,[0]),
        Script.op_read(apb.sram.data_inc.Address(),32,2),
        ],"ok",[(-1,0x1234567), (-1,0x2345678)])
    scripts["sram_long"] = ([
        Script.op_set("addr1",apb.sram.address.Address()>>8),
        Script.op_set("addr2",apb.sram.address.Address()>>16),
        Script.op_set("addr3",apb.sram.address.Address()>>24),
        Script.op_write(apb.sram.address.Address(),32,[0]),
        Script.op_write(apb.sram.data_window.Address()+0,32,[0x1, 0x2, 0x3, 0x4, 0x5], True),
        Script.op_write(apb.sram.data_window.Address()+4,32,[0x1234567, 0x2345678], True),
        Script.op_write(apb.sram.data_window.Address()+8,32,[0x9, 0xa, 0xb], True),
        Script.op_read(apb.sram.data_window.Address()+4,32,2,True),        
        Script.op_read(apb.sram.data_window.Address()+1,32,4,True),        
        ],"ok",[(-1,0x1234567),
                (-1,0x2345678),
                (-1,2),
                (-1,3),
                (-1,4),
                (-1,0x1234567),
                ])
    scripts_to_run = list(scripts.keys())
    #f invoke_script
    def invoke_script(self, script_name):
        script_to_run = self.compiled_scripts[script_name]
        bytes_to_run = bytearray(script_to_run[0].as_bytes())
        self.compare_expected("script master should start idle",
                              self.apb_script_resp__resp_type.value(), t_apb_script_master_resp_type["asm_resp_idle"] )

        self.apb_script_req__num_data_valid.drive(0)
        self.apb_script_req__op.drive(t_apb_script_master_op["asm_op_start_clear"] )
        self.bfm_wait(1)
        self.apb_script_req__op.drive(t_apb_script_master_op["asm_op_idle"] )
        self.bfm_wait(1)
        completion = "ok"
        data_returned = []
        cycles_to_run = 1000
        do_idle_cnt = self.inter_data_idle_cycles()
        while cycles_to_run > 0:
            bv = self.apb_script_resp__bytes_valid.value()
            data = self.apb_script_resp__data.value()
            if bv == 1: data_returned.append(data&0xff)
            if bv == 2: data_returned.append(data&0xffff)
            if bv == 3: data_returned.append(data&0xffffffff)
            if self.apb_script_resp__resp_type.value() != t_apb_script_master_resp_type["asm_resp_running"]:
                break
            bytes_consumed = self.apb_script_resp__bytes_consumed.value()
            for i in range(bytes_consumed):
                if len(bytes_to_run)>0:
                    bytes_to_run.pop(0)
                    pass
                do_idle_cnt = self.inter_data_idle_cycles()
                pass

            if do_idle_cnt > 0:
                self.apb_script_req__op.drive(t_apb_script_master_op["asm_op_idle"] )
                self.apb_script_req__data.drive(0xdeadbeef)
                self.apb_script_req__num_data_valid.drive(do_idle_cnt&7)
                self.bfm_wait(1)
                do_idle_cnt -= 1
                continue
                pass

            n = len(bytes_to_run)
            self.apb_script_req__op.drive(t_apb_script_master_op["asm_op_data"] )
            if n<=6:
                self.apb_script_req__op.drive(t_apb_script_master_op["asm_op_data_last"] )
                pass
            else:
                n = 6
                pass
            data = 0
            for i in range(n):
                data = data | (bytes_to_run[i] << (8*i))
                pass
            self.apb_script_req__data.drive(data)
            self.apb_script_req__num_data_valid.drive(n)
            self.bfm_wait(1)
            cycles_to_run -= 1
            pass
        completion = "unexpected"
        if self.apb_script_resp__resp_type.value() == t_apb_script_master_resp_type["asm_resp_completed"]:
            completion = "ok"
            pass
        if self.apb_script_resp__resp_type.value() == t_apb_script_master_resp_type["asm_resp_errored"]:
            completion = "errored"
            pass
        if self.apb_script_resp__resp_type.value() == t_apb_script_master_resp_type["asm_resp_poll_failed"]:
            completion = "poll_failed"
            pass
        if completion != script_to_run[1]:
            self.failtest("Completion that occured (%s) was not what was expected (%s)"%(completion, script_to_run[1]))
            pass
        self.verbose.info("Data returned by executing script %s"%str(data_returned))
        self.compare_expected("Data length that should have been read",
                              len(script_to_run[2]),
                              len(data_returned),
                              )
        for i in range(min(len(data_returned), len(script_to_run[2]))):
            d = data_returned[i]
            e = script_to_run[2][i]
            self.compare_expected("Data (masked) expected to be",
                                  e[1], d & e[0],
                              )
            
            pass
        self.bfm_wait(3)
        pass
    #f inter_data_idle_cycles
    def inter_data_idle_cycles(self) -> int:
        return 0
    #f run_init
    def run__init(self) -> None:
        self.random = Random()
        self.random.seed(self.random_seed)
        self.bfm_wait(2)
        self.compiled_scripts = {}
        for (n,s) in self.scripts.items():
            self.verbose.info("Compile script %s"%n)
            self.compiled_scripts[n] = (
                Script.compile_script(s[0]),
                s[1],
                s[2])
            pass
        pass
    def run(self) -> None:
        self.bfm_wait(10)
        for l in self.scripts_to_run:
            self.verbose.info("Run script %s"%l)
            self.invoke_script(l)
            pass
        self.passtest("Test succeeded")
        pass

#c ScriptMasterTest0
class ScriptMasterTest0(ScriptMasterTestBase):
    scripts_to_run = [  "timer_comparator",
                        "gpio_rw",
                        "sram",
                        "sram_gpio",
                        "sram_long",
                        "none",
    ]
    pass

#c ScriptMasterTest1
class ScriptMasterTest1(ScriptMasterTestBase):
    #f inter_data_idle_cycles
    def inter_data_idle_cycles(self) -> int:
        return 8
    scripts_to_run = [  "timer_comparator",
                        "gpio_rw",
                        "sram",
                        "sram_gpio",
                        "sram_long",
                        "none",
    ]
    pass

#c ScriptMasterTest2
class ScriptMasterTest2(ScriptMasterTestBase):
    #f inter_data_idle_cycles
    def inter_data_idle_cycles(self) -> int:
        return self.random.randrange(10)
    scripts_to_run = [  "timer_comparator",
                        "gpio_rw",
                        "sram",
                        "sram_gpio",
                        "sram_long",
                        "none",
    ]
    pass

#c ApbScriptMasterHardware
class ApbScriptMasterHardware(HardwareThDut):
    clock_desc = [("clk",(0,1,1))]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "tb_apb_script_master"
    dut_inputs  = {"apb_script_req":t_apb_script_master_request,
    }
    dut_outputs = {"apb_script_resp":t_apb_script_master_response,
                   "timer_equalled":3
    }
    loggers = { # "apb":{"modules":"dut dut.apb_log", "verbose":1},
                # "apb":{"modules":"dut.apb_log", "verbose":1},
                }
    def __init__(self, **kwargs):
        super(ApbScriptMasterHardware,self).__init__(**kwargs)
        pass
    pass

#c TestApbScriptMaster
class TestApbScriptMaster(TestCase):
    hw = ApbScriptMasterHardware
    _tests = {"fast": (ScriptMasterTest0, 100*1000, {"verbosity":0}),
              "slow": (ScriptMasterTest1, 100*1000, {"verbosity":0}),
              "random": (ScriptMasterTest2, 100*1000, {"verbosity":0}),
              "smoke": (ScriptMasterTest2, 100*1000, {"verbosity":0}),
              }
    pass


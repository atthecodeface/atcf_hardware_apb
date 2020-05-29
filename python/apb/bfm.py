#a Copyright
#  
#  This file 'bfm.py' copyright Gavin J Stark 2017-2020
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
from .structs import t_apb_request, t_apb_response
from cdl.utils   import csr

#a Test classes
#c ApbReg
class ApbReg(object):
    def __init__(self, apb:'ApbMaster', reg:csr.Csr):
        self.apb = apb
        self.reg = reg
        pass
    def read(self):
        return self.apb.read(self.reg.Address())
    def write(self, data):
        return self.apb.write(self.reg.Address(), data)
    pass

#c ApbMaster
class ApbMaster(object):
    def __init__(self, th:object, request_name:str, response_name:str):
        self.th = th
        for k in t_apb_request:
            setattr(self, k, getattr(th, "%s__%s"%(request_name, k)))
            pass
        for k in t_apb_response:
            setattr(self, k, getattr(th, "%s__%s"%(response_name, k)))
            pass
        self.psel.drive(0)
        self.penable.drive(0)
        self.paddr.drive(0)
        self.pwdata.drive(0)
        self.pwrite.drive(0)
        pass
    #f reg
    def reg(self, reg):
        return ApbReg(self, reg)
    #f transaction
    def transaction(self, write_not_read, address, data):
        self.psel.drive(1)
        self.penable.drive(0)
        self.paddr.drive(address)
        self.pwdata.drive(data)
        self.pwrite.drive(write_not_read)
        self.th.bfm_wait(1)
        self.penable.drive(1)
        self.th.bfm_wait(1)
        while self.pready.value()==0:
            self.th.bfm_wait(1)
            pass
        self.psel.drive(0)
        read_data = self.prdata.value()
        err       = self.perr.value()
        return (err, read_data)
    #f write
    def write(self, address, data, allow_error=False):
        (err, data) = self.transaction(1, address, data)
        if err and not allow_error:
            th.failtest("Expected apb error response of 0")
            pass
        pass
    #f read
    def read(self, address, allow_error=False):
        (err, data) = self.transaction(0, address, 0xdeadbeef)
        if err and not allow_error:
            th.failtest("Expected apb error response of 0")
            pass
        return data
    pass


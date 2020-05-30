#a Copyright
#  
#  This file 'target_timer.py' copyright Gavin J Stark 2020
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
from cdl.utils.csr   import Csr, CsrField, CsrFieldZero, Map, MapCsr

#a CSRs
class OutputReg(Csr):
    _fields = {}
    for i in range(16):
        _fields[2*i]   = CsrField(width=1, name="out%d"%i, doc="Output level for GPIO pin %d"%i)
        _fields[2*i+1] = CsrField(width=1, name="en%d"%i,  doc="Output enable for GPIO pin %d"%i)
        pass
    pass
class InputStatus(Csr):
    _fields = {0:  CsrField(width=16, name="value", doc="GPIO input pin levels"),
               16: CsrField(width=16, name="event", doc="GPIO input event status"),
              }
class InputReg0(Csr):
    _fields = {}
    for i in range(8):
        _fields[4*i]   =  CsrField(width=3, name="type%d"%i, doc="Type of GPIO input event")
        _fields[4*i+3] =  CsrFieldZero(width=1)
        pass
    pass
class InputReg1(Csr):
    _fields = {}
    for i in range(8):
        _fields[4*i]   =  CsrField(width=3, name="type%d"%(i+8), doc="Type of GPIO input event")
        _fields[4*i+3] =  CsrFieldZero(width=1)
        pass
    pass
class GpioAddressMap(Map):
    _map = [ MapCsr(reg=0, name="output", brief="out", csr=OutputReg, doc="GPIO output levels and enables"),
             MapCsr(reg=1, name="input_status", brief="sts", csr=InputStatus, doc="GPIO input pin levels and status of events"),
             MapCsr(reg=2, name="input0", brief="inp0", csr=InputReg0, doc="Type of GPIO input events (for pins 0-7)"),
             MapCsr(reg=3, name="input1", brief="inp1", csr=InputReg1, doc="Type of GPIO input events (for pins 8-15)"),
             ]

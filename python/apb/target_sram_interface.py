#a Copyright
#  
#  This file 'target_sram_interface.py' copyright Gavin J Stark 2020
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
class DataCsr(Csr):
    _fields = {0:  CsrField(width=32, name="value", brief="value", doc="SRAM memory contents"),
              }
class AddressCsr(Csr):
    _fields = {0:  CsrField(width=32, name="value", brief="value", doc="SRAM address to access; this is a 32 bit field, but the SRAM will have fewer address lines, and the top bits will be ignored"),
              }
class ControlCsr(Csr):
    _fields = {0:  CsrField(width=32, name="value", brief="value", doc="32-bit application-specific control register; this is used by the system that this register is connected to"),
              }

class SramInterfaceAddressMap(Map):
    _map = [ MapCsr(reg=0,   name="address",     brief="adr",  csr=AddressCsr, doc="Address of SRAM to access"),
             MapCsr(reg=1,   name="data",        brief="data", csr=DataCsr,    doc="Data of SRAM at address; reading/writing causes an SRAM access"),
             MapCsr(reg=2,   name="control",     brief="ctl",  csr=ControlCsr, doc="Control register for the SRAM"),
             MapCsr(reg=4,   name="data_inc",    brief="dinc", csr=DataCsr,    doc="Autoincrement data access - Address increments by one after each access; read/writing causes an SRAM access"),
             MapCsr(reg=128, name="data_window", brief="dwin", csr=DataCsr,    doc="Windowed access - bottom bits of register are used as bottom bits of SRAM address; reading/writing causes an SRAM access"),
             ]
             

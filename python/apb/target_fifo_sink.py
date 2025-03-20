#a Imports
from cdl.utils.csr   import Csr, CsrField, CsrFieldZero, Map, MapCsr

#a CSRs
class DataCsr(Csr):
    _fields = {0:  CsrField(width=32, name="value", brief="value", doc="SRAM memory contents"),
              }
class ConfigStatusCsr(Csr):
    _fields = {0:  CsrField(width=32, name="value", brief="value", doc="Configuration / status"),
              }
class FifoSinkAddressMap(Map):
    _map = [ MapCsr(reg=0,   name="config_status",  brief="cs",     csr=ConfigStatusCsr, doc="Config/Status"),
             MapCsr(reg=1,   name="fifo_status", brief="status", csr=DataCsr, doc="Fifo Status"),
             MapCsr(reg=2,   name="fifo_data",   brief="data",   csr=DataCsr, doc="Data from the FIFO"),
             ]
             

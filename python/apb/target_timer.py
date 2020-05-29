from cdl.utils.csr   import Csr, CsrField, CsrFieldZero, Map, MapCsr

class TimerCsr(Csr):
    _fields = {0:  CsrField(width=31, name="value", brief="value", doc="31-bit timer value"),
              31: CsrFieldZero(width=1),
              }
class TimerComparatorCsr(Csr):
    _fields = {0:  CsrField(width=31, name="comparator", brief="cmp", doc="31-bit timer comparator value"),
               31: CsrField(name="equalled", brief="eq", doc="Asserted if the timer counter value has equalled the 31-bit comparator value"),
              }

class TimerAddressMap(Map):
    _map = [ MapCsr(reg=0, name="timer", brief="tmr", csr=TimerCsr, doc=""),
             MapCsr(reg=1, name="comparator0", brief="cmp0", csr=TimerComparatorCsr, doc=""),
             MapCsr(reg=2, name="comparator1", brief="cmp1", csr=TimerComparatorCsr, doc=""),
             MapCsr(reg=3, name="comparator2", brief="cmp2", csr=TimerComparatorCsr, doc=""),
             ]
             

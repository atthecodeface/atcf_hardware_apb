#a Copyright
#  
#  This file 'bfm.py' copyright Gavin J Stark 2017-2020
#  
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, version 2.0.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#  for more details.

#a Imports
from .structs import apb_request, apb_response

#a Test classes
#c ApbMaster
class ApbMaster(object):
    def __init__(self, th:object, request_name:str, response_name:str):
        for k in apb_request:
            setattr(self, k, getattr(th, "%s__%s"%(request_name, k)))
            pass
        for k in apb_response:
            setattr(self, k, getattr(th, "%s__%s"%(response_name, k)))
            pass
        self.psel.drive(0)
        self.penable.drive(0)
        self.paddr.drive(0)
        self.pwdata.drive(0)
        self.pwrite.drive(0)
        pass
    #f write
    def write(self, address, data):
        self.psel.drive(1)
        self.penable.drive(0)
        self.paddr.drive(address)
        self.pwdata.drive(data)
        self.pwrite.drive(1)
        th.bfm_wait(1)
        self.penable.drive(1)
        th.bfm_wait(1)
        while self.pready.value()==0:
            th.bfm_wait(1)
            pass
        self.psel.drive(0)
        pass
    #f read
    def read(self, address):
        self.psel.drive(1)
        self.penable.drive(0)
        self.paddr.drive(address)
        self.pwdata.drive(0xdeadbeef)
        self.pwrite.drive(0)
        self.bfm_wait(1)
        self.penable.drive(1)
        th.bfm_wait(1)
        while self.pready.value()==0:
            th.bfm_wait(1)
            pass
        self.psel.drive(0)
        return self.prdata.value()

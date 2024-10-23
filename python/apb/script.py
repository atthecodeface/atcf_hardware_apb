#!/usr/bin/env python3
from cdl.utils.memory import Memory
from typing import Dict, List, Tuple

#a Classes
class CompiledScript(object):
    contents:List[List[int]]
    def __init__(self):
        self.contents = []
        pass
    def add_contents(self, op:List[int]) -> None:
        self.contents.append(op)
        pass
    def as_bytes(self) -> bytes:
        r = bytearray()
        for op in self.contents:
            for b in op:
                r.append(b)
                pass
            pass
        return bytes(r)
    pass
#c Script
class Script(object):
    opcodes = {
        "opcode_class_set": 0,
        "opcode_class_poll": 1,
        "opcode_class_read": 2,
        "opcode_class_write": 3,
        }

    opcode_subclass = {
        "set_addr1": 1,
        "set_addr2": 2,
        "set_addr3": 3,
        "set_poll_delay": 8,
        "set_poll_count": 12,

        "poll_clr": 0,
        "poll_set": 64,

        "data_size_8": 0,
        "data_size_16": 1,
        "data_size_32": 2,
        "inc": 32,
        "poll_set": 64,
        }
    #f get_define_int
    @staticmethod
    def get_define_int(defines, k, default):
        if k in defines:
            return int(defines[k],0)
        return default
    
    #f op_set
    @classmethod
    def op_set(cls, set_op, data):
        return [(cls.opcodes["opcode_class_set"]<<6) | cls.opcode_subclass["set_"+set_op],
                data&0xff]
    #f op_poll_clr
    @classmethod
    def op_poll_set(cls, addr8, bit=0):
        return [(cls.opcodes["opcode_class_poll"]<<6) |
                cls.opcode_subclass["poll_clr"] |
                (bit & 31),
                addr8&0xff]
    #f op_poll_set
    @classmethod
    def op_poll_set(cls, addr8, bit=0):
        return [(cls.opcodes["opcode_class_poll"]<<6) |
                cls.opcode_subclass["poll_set"] |
                (bit & 31),
                addr8&0xff]
    #f op_read
    @classmethod
    def op_read(cls, addr8, data_size, num=1, inc=False):
        opts = 0
        if inc: opts = cls.opcode_subclass["inc"]
        return [(cls.opcodes["opcode_class_read"]<<6) |
                opts |
                cls.opcode_subclass["data_size_"+str(data_size)] |
                (((num%8)-1) << 2),
                addr8&0xff]
    #f op_write
    @classmethod
    def op_write(cls, addr8, data_size, data=[], inc=False):
        opts = 0
        if inc: opts = cls.opcode_subclass["inc"]
        num = len(data)
        if num==0 or num>8:
            return []
        r = []
        r.append( (cls.opcodes["opcode_class_write"]<<6) |
                  opts |
                  cls.opcode_subclass["data_size_"+str(data_size)] |
                  ((num-1) << 2) )
        r.append(addr8&0xff)
        db = data_size // 8
        for d in data:
            for i in range(db):
                r.append(d&0xff)
                d = d>>8
                pass
            pass
        return r
    #f compile_script
    @staticmethod
    def compile_script(script):
        """
        Compile of a script (single pass)

        Script is op*
        
        An op is
        op_set("addr1|addr2|addr3|poll_delay|poll_count",data)
        op_poll_clr(addr,bit)
        op_poll_set(addr,bit)
        op_read(addr,8|16|32,[N])
        op_write(addr,8|16|32,data_list)
        """
        compiled = CompiledScript()
        for op in script:
            compiled.add_contents(op)
            pass
        return compiled
    pass
    

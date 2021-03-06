#!/usr/bin/env python3
from cdl.utils.memory import Memory
from typing import Dict, List, Tuple

#a Classes
class CompiledProgam(object):
    labels:Dict[str,int]
    contents:List[Tuple[int,int]]
    def __init__(self):
        self.labels = {}
        self.contents = []
        pass
    def add_label(self, name:str, address:int) -> None:
        self.labels[name] = address
        pass
    def add_contents(self, address:int, data:int) -> None:
        self.contents.append((address,data))
        pass
    def add_to_memory(self, memory:Memory, bytes_per_word=8, label_prefix:str="", base_address:int=0) -> None:
        for (ln, la) in self.labels.items():
            memory.add_label( label="%s%s"%(label_prefix, ln),
                              address=la )
            pass
        for (a,d) in self.contents:
            memory.add_data_word(address=(a + base_address)*bytes_per_word,
                                 data=d)
            pass
        pass
    pass
#c Rom
class Rom(object):
    opcodes = {
        "opcode_class_alu": 0,
        "opcode_class_set_parameter": 1,
        "opcode_class_apb_request": 2,
        "opcode_class_branch": 3,
        "opcode_class_wait": 4,
        "opcode_class_finish": 5
        }

    opcode_subclass = {
        "rom_op_alu_or": 0,
        "rom_op_alu_and": 1,
        "rom_op_alu_bic": 2,
        "rom_op_alu_xor": 3,
        "rom_op_alu_add": 4,

        "rom_op_set_address": 0,
        "rom_op_set_repeat": 1,
        "rom_op_set_accumulator": 2,
        "rom_op_set_increment": 3,

        "rom_op_branch": 0,
        "rom_op_beq": 1,
        "rom_op_bne": 2,
        "rom_op_loop": 3,
        "rom_op_branch_link": 4,
        "rom_op_beq_link": 5,
        "rom_op_bne_link": 6,
        "rom_op_ret": 7,

        "rom_op_req_read": 0,
        "rom_op_req_write_arg": 1,
        "rom_op_req_write_acc": 2,
        "rom_op_req_read_inc": 4, # auto-increment
        "rom_op_req_write_arg_inc": 5,
        "rom_op_req_write_acc_inc": 6,
        }
    #f get_define_int
    @staticmethod
    def get_define_int(defines, k, default):
        if k in defines:
            return int(defines[k],0)
        return default
    
    #f op_alu
    @classmethod
    def op_alu(cls, alu_op, data):
        return (cls.opcodes["opcode_class_alu"]<<(32+5)) | (cls.opcode_subclass["rom_op_alu_"+alu_op]<<32) | data
        pass
    #f op_branch
    @classmethod
    def op_branch(cls, branch_op, data):
        return (cls.opcodes["opcode_class_branch"]<<(32+5)) | (cls.opcode_subclass["rom_op_"+branch_op]<<32) | data
        pass
    #f op_set
    @classmethod
    def op_set(cls, set_op, data):
        return (cls.opcodes["opcode_class_set_parameter"]<<(32+5)) | (cls.opcode_subclass["rom_op_set_"+set_op]<<32) | data
        pass
    #f op_req
    @classmethod
    def op_req(cls, req_op, data):
        return (cls.opcodes["opcode_class_apb_request"]<<(32+5)) | (cls.opcode_subclass["rom_op_req_"+req_op]<<32) | data
        pass
    #f op_wait
    @classmethod
    def op_wait(cls, data):
        return (cls.opcodes["opcode_class_wait"]<<(32+5)) | data
        pass
    #f op_finish
    @classmethod
    def op_finish(cls):
        return (cls.opcodes["opcode_class_finish"]<<(32+5))
        pass
    #f compile_program
    @staticmethod
    def compile_program(program, address=0):
        """
        Does a two-pass compile of a program

        A program consists of a list of (op | (op*labels tuple))

        labels is a list of label string

        A label string can be a 'set label' if it ends in a colon e.g. 'retry:'
        A label string is otherwise a 'use label as data'

        An op is
        op_alu("or|and|bic|xor|add",data)
        op_branch("branch|beq|bne|loop",data)
        op_set("address|repeat|accumulator",data)
        op_req("read|write_arg|write_acc|read_inc|write_arg_inc|write_acc_inc",data)
        op_wait(data)
        op_finish()

        inc is a post-increment
        """
        compiled = CompiledProgam()
        label_addresses = {}
        for p in range(2):
            prog_address = address
            for op_labels in program["code"]:
                if len(op_labels)==1:
                    op=op_labels[0]
                    labels=[]
                    pass
                else:
                    (op,labels) = op_labels
                    pass
                if p==0:
                    for l in labels:
                        if l[-1]==':': label_addresses[l] = prog_address
                        pass
                    pass
                else:
                    for l in labels:
                        if l[-1]!=':':
                            op |= label_addresses[l+":"]
                            # print("%08x"%label_addresses[l+":"])
                            pass
                        pass
                    compiled.add_contents(prog_address, op)
                    pass
                prog_address = prog_address + 1
                pass
            pass
        for (ln,la) in label_addresses.items():
            compiled.add_label(ln, la)
            pass
        return compiled
    pass
    #f mif_of_compilation
    @staticmethod
    def open_filename(filename):
        import sys
        if filename=='': return (sys.stdout, lambda x:None)
        f = open(filename,"w")
        if not f:
            die
            pass
        return (f, lambda x:f.close() )
    @classmethod
    def mif_of_compilation(cls, compiled, filename=''):
        (f,c) = cls.open_filename(filename)
        memory = Memory(bit_width=40)
        compiled.add_to_memory(memory, bytes_per_word=5)
        memory.write_mif(f)
        c(None)
        pass
    @classmethod
    def mem_of_compilation(cls, compiled, filename=''):
        (f,c) = cls.open_filename(filename)
        memory = Memory(bit_width=40)
        compiled.add_to_memory(memory, bytes_per_word=5)
        memory.write_mem(f)
        c(None)
        pass


#!/usr/bin/env python3
tb_apb_timer_timer        = 0x00000000
tb_apb_timer_comparator_0 = 0x00000004
tb_apb_timer_comparator_1 = 0x00000005
tb_apb_timer_comparator_2 = 0x00000006
tb_apb_gpio_output_reg    = 0x10000000
tb_apb_gpio_input_status  = 0x10000004
tb_apb_gpio_input_reg_0   = 0x10000008
tb_apb_gpio_input_reg_1   = 0x1000000c

def program(apb_rom, defines):
    """
    There are multiple programs

    The first is at 0, which is just finish

    The second is at 1, which tests the GPIO and timer
    """
    program = {}
    program["code"] = []
    program["code"] += [
        (apb_rom.op_finish(),),
        ]
    program["code"] += [
        (apb_rom.op_set("address",tb_apb_gpio_output_reg),),
        (apb_rom.op_req("write_arg",0xffffffff),),
        (apb_rom.op_req("read",0),),
        (apb_rom.op_branch("beq",0),["fail"]),
        (apb_rom.op_alu("add",1),),
        (apb_rom.op_branch("bne",0),["fail"]),
        (apb_rom.op_set("address",tb_apb_timer_timer),),
        (apb_rom.op_req("read",0),),
        (apb_rom.op_alu("add",40),),
        (apb_rom.op_set("address",tb_apb_timer_comparator_0),),
        (apb_rom.op_req("write_acc",0),),
        (apb_rom.op_req("read",0),["read_loop:"]),
        (apb_rom.op_alu("and",0x80000000),),
        (apb_rom.op_branch("beq",0),["read_loop"]),
        ]
    program["code"] += [
        (apb_rom.op_finish(),),
        ]
    program["code"] += [
        (apb_rom.op_branch("branch",0),["fail:","fail"]),
        ]
    return program

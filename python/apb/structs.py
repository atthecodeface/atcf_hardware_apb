#t t_apb_request
t_apb_request = {
    "paddr":32,
    "penable":1,
    "psel":1,
    "pwrite":1,
    "pwdata":32,
}

#t t_apb_response
t_apb_response = {
    "prdata":32,
    "pready":1,
    "perr":1,
}

#t t_apb_processor_response
t_apb_processor_response = {
    "acknowledge":1,
    "rom_busy":1,
}

#t t_apb_processor_request
t_apb_processor_request = {
    "valid":1,
    "address":16,
}

#t t_apb_rom_request
t_apb_rom_request = {
    "enable":1,
    "address":16,
}

#t t_apb_script_master_op
t_apb_script_master_op = {
    "asm_op_idle":0,
    "asm_op_start":1,
    "asm_op_start_clear":2,
    "asm_op_data":3,
    "asm_op_data_last":4,
} 

# t_apb_script_master_resp_type
t_apb_script_master_resp_type = {
    "asm_resp_idle":0,
    "asm_resp_running":1,
    "asm_resp_completed":2,
    "asm_resp_poll_failed":3,
    "asm_resp_errored":4,
}

# t_apb_script_master_request
t_apb_script_master_request = {
    "op": 3, # t_apb_script_master_op
    "num_data_valid": 3, # Number of bytes valid, 0 to 6, in data; ignored if not an op data
    "data":48,
} 

# t_apb_script_master_response
t_apb_script_master_response  = {
    "resp_type":3,
    "bytes_consumed":3, # If non-zero then remove the bottom bytes from the data request in the next cycle; data is never consumed in back-to-back cycles, and this will be zero for one cycle after it is nonzero";
    "bytes_valid":2, # // 1, 2, or 3 for 32-bit; 0 for no valid data
    "data":32,
}


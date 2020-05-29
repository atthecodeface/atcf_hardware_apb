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


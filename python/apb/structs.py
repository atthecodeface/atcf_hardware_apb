#t apb_request
apb_request = {
    "paddr":32,
    "penable":1,
    "psel":1,
    "pwrite":1,
    "pwdata":32,
}

#t apb_response
apb_response = {
    "prdata":32,
    "pready":1,
    "perr":1,
}

#t apb_processor_response
apb_processor_response = {
    "acknowledge":1,
    "rom_busy":1,
}

#t apb_processor_request
apb_processor_request = {
    "valid":1,
    "address":16,
}

#t apb_rom_request
apb_rom_request = {
    "enable":1,
    "address":16,
}


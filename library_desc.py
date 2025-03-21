import cdl_desc
from cdl_desc import CdlModule, CModel

class Library(cdl_desc.Library):
    name = "apb"
    pass

class ApbModules(cdl_desc.Modules):
    name = "apb"
    c_src_dir   = "cmodel"
    src_dir     = "cdl"
    tb_src_dir  = "tb_cdl"
    libraries = {"std": True, "utils": True, }
    cdl_include_dirs = ["cdl"]
    export_dirs      = cdl_include_dirs + [ src_dir ]
    modules = []
    modules += [ CdlModule("apb_logging") ]
    modules += [ CdlModule("apb_master_mux") ]
    modules += [ CdlModule("apb_processor") ]
    modules += [ CdlModule("apb_script_master") ]
    modules += [ CdlModule("apb_target_gpio") ]
    modules += [ CdlModule("apb_target_timer") ]
    modules += [ CdlModule("apb_target_fifo_sink") ]
    modules += [ CdlModule("apb_target_sram_interface") ]
    modules += [ CdlModule("csr_master_apb") ]
    modules += [ CdlModule("csr_target_apb") ]
    modules += [ CdlModule("csr_target_csr") ]
    modules += [ CdlModule("csr_target_timeout") ]
    modules += [ CdlModule("tb_apb_processor",src_dir=tb_src_dir) ]
    modules += [ CdlModule("tb_apb_script_master",src_dir=tb_src_dir) ]
    modules += [ CdlModule("tb_apb_sram_interface",src_dir=tb_src_dir) ]
    modules += [ CdlModule("tb_apb_fifo_sink",src_dir=tb_src_dir) ]
    pass

    

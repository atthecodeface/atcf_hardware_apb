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
    include_dir = "cdl"
    libraries = {"std": True, }
    export_dirs = [ src_dir, include_dir ]
    modules = []
    modules += [ CdlModule("apb_logging") ]
    modules += [ CdlModule("apb_master_mux") ]
    modules += [ CdlModule("apb_processor") ]
    modules += [ CdlModule("apb_target_gpio") ]
    modules += [ CdlModule("apb_target_timer") ]
    modules += [ CdlModule("tb_apb_processor",src_dir=tb_src_dir) ]
    pass

    

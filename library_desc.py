import cdl_desc
from cdl_desc import CdlModule, CModel

class ApbModules(cdl_desc.Modules):
    name = "apb"
    c_src_dir   = "cmodel"
    src_dir     = "cdl"
    tb_src_dir  = "cdl_tb"
    include_dir = "cdl"
    libraries = ["timer"]
    modules = []
    modules += [ CdlModule("apb_logging") ]
    modules += [ CdlModule("apb_master_mux") ]
    modules += [ CdlModule("apb_processor") ]
    modules += [ CdlModule("apb_target_gpio") ]
    modules += [ CdlModule("apb_target_timer") ]
    modules += [ CdlModule("tb_apb_processor",src_dir=tb_src_dir) ]
    modules += [ CModel("srams",src_dir=c_src_dir) ]
    pass

modules=cdl_desc.Modules.__subclasses__

#!/usr/bin/env python3
from apb import Rom

#a Toplevel
if __name__ == "__main__":
    import argparse, sys, re
    parser = argparse.ArgumentParser(description='Generate MIF or READMEMH files for APB processor ROM')
    parser.add_argument('--src', type=str, default=None,
                    help='Source for APB ROM')
    parser.add_argument('--mif', type=str, default=None,
                    help='Output MIF filename')
    parser.add_argument('--mem', type=str, default=None,
                    help='Output READMEMH filename')
    parser.add_argument('--define', type=str, action='append', default=[],
                    help='Defines for the ROM program')
    args = parser.parse_args()
    show_usage = False
    if args.src is None:
        show_usage = True
        pass
    if show_usage:
        parser.print_help()
        sys.exit(0)
        pass
    defines = {}
    dre = re.compile(r"(.*)=(.*)")
    for d in args.define:
        m = dre.match(d)
        if m is None:
            defines[d] = True
            pass
        else:
            defines[m.group(1)] = m.group(2)
            pass
        pass
    import importlib
    m = importlib.import_module(args.src)
    program = m.program(Rom, defines)
    compilation = Rom.compile_program(program)
    if args.mif is not None:
        Rom.mif_of_compilation(compilation, filename=args.mif)
        pass
    if args.mem is not None:
        Rom.mem_of_compilation(compilation, filename=args.mem)
        pass
    pass

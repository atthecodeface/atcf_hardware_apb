Q=@

smoke: smoke_mifs
	${Q}${SIM} smoke.csm

smoke_mifs: smoke_rom.py
	${Q}PYTHONPATH=.:${PYTHONPATH} apb_processor_rom.py --src smoke_rom --mif smoke_rom.mif

.PHONY:python
python:
	PYTHONPATH=${BUILD_ROOT}:${CDL_ROOT}/lib/cdl/python:${SRC_ROOT}/python:${PYTHONPATH} python3 -m python.regress -v

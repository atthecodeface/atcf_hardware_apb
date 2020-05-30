Q=@
CDL_REGRESS = ${CDL_ROOT}/libexec/cdl/cdl_regress.py

.PHONY:regression regression_batch regression_python
.PHONY:smoke smoke_batch smoke_python

smoke: smoke_batch smoke_python

smoke_batch: smoke_mifs
	${Q}${SIM} smoke.csm
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} --package-dir regress:${SRC_ROOT}/python --suite-dir=python --only-tests 'simple' test_timer

smoke_mifs: smoke_rom.py
	${Q}PYTHONPATH=.:${PYTHONPATH} PATH=${SRC_ROOT}/python:${PATH} apb_processor_rom.py --src smoke_rom --mif smoke_rom.mif

.PHONY:regress
regress:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} --package-dir regress:${SRC_ROOT}/python --suite-dir=python test_timer

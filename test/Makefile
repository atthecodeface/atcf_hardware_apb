Q=@
CDL_REGRESS = ${CDL_ROOT}/libexec/cdl/cdl_regress.py

smoke: smoke_mifs
	${Q}${SIM} smoke.csm
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} --package-dir regress:${SRC_ROOT}/python --suite-dir=python --only-tests 'test_comparator' test_i2c

smoke_mifs: smoke_rom.py
	${Q}PYTHONPATH=.:${PYTHONPATH} apb_processor_rom.py --src smoke_rom --mif smoke_rom.mif

.PHONY:regress
regress:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} --package-dir regress:${SRC_ROOT}/python --suite-dir=python peripherals


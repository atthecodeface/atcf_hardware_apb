Q=@
CDL_REGRESS = ${CDL_ROOT}/libexec/cdl/cdl_regress.py

.PHONY:regression regression_batch regression_python
.PHONY:smoke smoke_batch smoke_python

# $ WAVES=--waves=dut SMOKE_OPTIONS=--only-tests='0' SMOKE_TESTS=test_fifo_sink grip make repo.atcf_hardware_apb.smoke_test
WAVES ?=

SMOKE_OPTIONS ?= --only-tests 'smoke'
SMOKE_TESTS   ?= test_timer test_processor test_script test_fifo_sink test_sram_interface
REGRESS_TESTS ?= test_timer test_processor test_script test_fifo_sink test_sram_interface
CDL_REGRESS_PACKAGE_DIRS = --package-dir regress:${SRC_ROOT}/python  --package-dir regress:${GRIP_ROOT_PATH}/atcf_hardware_utils/python --package-dir regress:${GRIP_ROOT_PATH}/atcf_hardware_apb/python

.PHONY:smoke
smoke:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT}  ${CDL_REGRESS_PACKAGE_DIRS} --suite-dir=python ${SMOKE_OPTIONS} ${SMOKE_TESTS} ${WAVES}

.PHONY:regress
regress:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} ${CDL_REGRESS_PACKAGE_DIRS} --suite-dir=python ${REGRESS_TESTS}

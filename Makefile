CDL_ROOT=/Users/gavinprivate/Git/cdl_tools_grip/tools
include ${CDL_ROOT}/lib/cdl/cdl_templates.mk
SRC_ROOT   = $(abspath ${CURDIR})
OTHER_SRCS = ${SRC_ROOT}/*
BUILD_ROOT = ${SRC_ROOT}/build

all: sim

smoke: sim
	(cd test && PATH=${SRC_ROOT}/python:${PATH} ${MAKE} SIM=${SIM} smoke)

-include ${BUILD_ROOT}/Makefile

makefiles:
	${CDL_LIBEXEC_DIR}/cdl_desc.py --require ${SRC_ROOT} --build_root ${BUILD_ROOT} ${OTHER_SRCS}

clean:
	mkdir -p ${BUILD_ROOT}

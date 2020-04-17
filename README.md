# atcf_hardware_std

This repository contains the ATCF APB/CSR infrastructure CDL modules.

The APB (AMBA Peripheral Bus) is a simple standard bus protocol for connecting
peripherals to a single master.

## Status

The repository is in use in two grip repositories: for the BBC
microcomputer and for RISC-V systems. They are very stable.

# APB targets

The modules in this repository include simple targets for a timer and
gpio, and a logging module to help debug simulations.

# APB bus master multiplexer

There is also a two master APB multiplexer, which permits two bus masters to share an APB.

# APB bus master processor

There is the APB processor module, which takes a program in an SRAM
(or ROM) which provides a programmable bus master for the APB. The
purpose of this module is to provide hardware initialization time
configuration of APB peripherals using a ROM program that may be
supplied (in FPGA) at build time, or in silicon perhaps from a
configuration ROM. The processor includes a 32-bit accumulator and
very simple ALU, and the processor supports simple branching and
looping. This permits, for example, a polling loop to wait for a PLL
to lock, with APB read accesses polling the lock bit.

# CSR bus system (pipelined APB bus extension)

There is also the CSR bus system, which provides a way to extend the
APB using many clock ticks and register stages across an FPGA or
silicon device. This was used in the original GIP implementations in
the early 2000s, and it permits a design to have a CSR interface
without fear that the peripheral access will impose timing constraints
on that design.

## csr_target_apb

The CSR bus system has an APB target - to CSR master
bridge, which is the source of the CSR bus. This takes all the APB
accesses with the select signal and presents them as 16-bit select,
16-bit address accesses on the pipelined CSR bus.

## csr_master_apb

The CSR bus system provides an endpoint that is an APB master - so
standard APB peripherals can be connected. This provides a 16-bit
address to the peripheral, for a CSR bus access to a specified 16-bit
select.

## csr_target_csr

The CSR bus system can terminate in this module which provides a
simple synchronous access request - address, select, read_not_write,
data, and takes read data in response on the following cycle. This is
the simplest mechanism for connecting to the CSR bus system.

## csr_target_timeout

The CSR bus system suports a tree structure, and the master cannot
tell if a CSR bus request will be accepted by any of the targets on
the tree. This module should be instantiated on the tree to accept any
transaction that has not been accepted within a specified timeout (256
cycles is plenty, usually).




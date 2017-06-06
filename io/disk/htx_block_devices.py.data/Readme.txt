HTX [Hardware Test eXecutive] is a test tool suite, which is used by various
System p validation labs to verify the System p hardware design. It is used
during processor bring up, hardware system integration, I/O Verification(IOV),
Characterization and Manufacturing. The goal of HTX is to stress test the
system by exercising all hardware components concurrently in order to uncover
any hardware design flaws and hardware hardware or hardware-software 
interaction issues. HTX runs on AIX, Bare Metal Linux(BML) and distribution
Linux. HTX offers a light weight HTX daemon (HTXD) which support command line
interface and menu based user interactive interface.

The test also changes SMT values while HTX is running, based on input from the
user in yaml file.

Inputs:
------
disk: '/dev/sdb /dev/sdc'
time_limit: 2 (In hours)
mdt_file: 'mdt.io'
smt_change: True or False

from circuit import Circuit
import sys

design = sys.argv[1]
cir = Circuit(design)

f1 = design + "/" + design + ".v"
cir.parseVerilog(f1)
f2 = design + "/die0.rpt"
cir.parsePartition(f2)

if len(sys.argv) == 3:
	cir.parseSTIL(sys.argv[2], False)
	#cir.dumpWorstSTIL(sys.argv[2])
else:
	f3 = design + "/" + design + "_xfill.stil"
	cir.parseSTIL(f3)
	cir.dumpSTIL(f3)

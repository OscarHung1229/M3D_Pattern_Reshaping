from circuit import Circuit
import sys
import numpy as np

design = sys.argv[1]
cir = Circuit(design)

f1 = design + "/" + design + ".v"
cir.parseVerilog(f1)
f2 = design + "/die0.rpt"
cir.parsePartition(f2)

keyword = sys.argv[3]
if "wsa" in keyword:
	cir.parseSTIL(sys.argv[2], 0)
	cir.dumpWorstSTIL(sys.argv[2])
	arr = np.array(cir.WSA)
	print("Mean WSA: {0}".format(np.mean(arr)))
	print("Stdev WSA: {0}".format(np.std(arr)))
elif "sta" in keyword:
	cir.parseSTIL(sys.argv[2], 1)
	cir.dumpWorstSTIL(sys.argv[2])
	arr = np.array(cir.WSA)
	print("Mean WSA: {0}".format(np.mean(arr)))
	print("Stdev WSA: {0}".format(np.std(arr)))

elif "prefer" in keyword:
	f3 = design + "/" + design + "_xfill.stil"
	cir.parseSTIL(sys.argv[2], 2)
	cir.dumpPreferSTIL(sys.argv[2])
elif "sa" in keyword:
	f3 = design + "/" + design + "_xfill.stil"
	cir.parseSTIL(sys.argv[2], 3)
	cir.dumpSASTIL(sys.argv[2])
elif "ilp" in keyword:
	f3 = design + "/" + design + "_xfill.stil"
	cir.parseSTIL(sys.argv[2], 4)
	#cir.dumpILPSTIL(sys.argv[2])


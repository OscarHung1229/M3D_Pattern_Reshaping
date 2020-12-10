import sys
from operator import itemgetter	

#Global matrix for signal propagation
NotMap = [1, 0, 2, 4, 3]
AndMap = [
	[0, 0, 0, 0, 0],
	[0, 1, 2, 3, 4],
	[0, 2, 2, 2, 0],
	[0, 3, 2, 3, 0],
	[0, 4, 0, 0, 4]
] 
OrMap = [
	[0, 1, 2, 3, 4],
	[1, 1, 1, 1, 1],
	[2, 1, 2, 1, 2],
	[3, 1, 1, 3, 1],
	[4, 1, 2 ,1 ,4]
]

XorMap = [
	[0, 1, 2, 3, 4],
	[1, 0, 2, 4, 3],
	[2, 2, 2, 2, 2],
	[3, 4, 2, 0, 1],
	[4, 3, 2, 1, 0]
]


class Gate:
	def __init__(self, gtype, name):
		self.gtype = gtype			#Gate type
	 	self.level = -1					#Level in the circuit
	 	self.name = name				#Gate name
	 	self.pins = {}					#Input/Output pins
		
	def add_pins(self, ptype, wire):
		self.pins[ptype] = wire
	def set_level(self,l):
		self.level = l
	

	def eval(self):
		value = -1
		if "AND" in self.gtype:
			for p in self.pins:
				pin = self.pins[p]
				if "Z" in pin.name:
					continue
				if value == -1:
					value = pin.value
				else:
					value = AndMap[value][pin.value]
			if "NAND" in self.gtype:
				self.pins["ZN"].set_value(NotMap[value])
			else: 
				self.pins["ZN"].set_value(value)

		elif self.gtype.startswith("OR") or self.gtype.startswith("NOR"):
			for p in self.pins:
				pin = self.pins[p]
				if "Z" in pin.name:
					continue
				if value == -1:
					value = pin.value
				else:
					value = OrMap[value][pin.value]
			if "NOR" in self.gtype:
				self.pins["ZN"].set_value(NotMap[value])
			else: 
				self.pins["ZN"].set_value(value)
		
		elif self.gtype.startswith("XOR"):
			self.pins["Z"].set_value(XorMap[self.pins["A"].value][self.pins["B"].value])
			
		elif self.gtype.startswith("XNOR"):
			self.pins["ZN"].set_value(NotMap[XorMap[self.pins["A"].value][self.pins["B"].value]])

		elif self.gtype.startswith("AOI21_"):
			value = AndMap[self.pins["B1"].value][self.pins["B2"].value]
			value = OrMap[self.pins["A"].value][value]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("AOI22_"):
			v1 = AndMap[self.pins["B1"].value][self.pins["B2"].value]
			v2 = AndMap[self.pins["A1"].value][self.pins["A2"].value]
			value = OrMap[v1][v2]
			self.pins["ZN"].set_value(NotMap[value])
			
		elif self.gtype.startswith("AOI211_"):
			value = AndMap[self.pins["C1"].value][self.pins["C2"].value]
			value = OrMap[self.pins["B"].value][value]
			value = OrMap[self.pins["A"].value][value]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("AOI221_"):
			v1 = AndMap[self.pins["C1"].value][self.pins["C2"].value]
			v2 = AndMap[self.pins["B1"].value][self.pins["B2"].value]
			value = OrMap[self.pins["A"].value][v1]
			value = OrMap[v2][value]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("AOI222_"):
			v1 = AndMap[self.pins["C1"].value][self.pins["C2"].value]
			v2 = AndMap[self.pins["B1"].value][self.pins["B2"].value]
			v3 = AndMap[self.pins["A1"].value][self.pins["A2"].value]
			value = OrMap[v1][v2]
			value = OrMap[v3][value]
			self.pins["ZN"].set_value(NotMap[value])
				
		elif self.gtype.startswith("OAI21_"):
			v1 = OrMap[self.pins["B1"].value][self.pins["B2"].value]
			value = AndMap[v1][self.pins["A"].value]	
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("OAI22_"):
			v1 = OrMap[self.pins["B1"].value][self.pins["B2"].value]
			v2 = OrMap[self.pins["A1"].value][self.pins["A2"].value]
			value = AndMap[v1][v2]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("OAI211_"):
			v1 = OrMap[self.pins["C1"].value][self.pins["C2"].value]
			value = AndMap[v1][self.pins["A"].value]	
			value = AndMap[value][self.pins["B"].value]	
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("OAI221_"):
			v1 = OrMap[self.pins["C1"].value][self.pins["C2"].value]
			v2 = OrMap[self.pins["B1"].value][self.pins["B2"].value]
			value = AndMap[v1][self.pins["A"].value]	
			value = AndMap[value][v2]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("OAI222_"):
			v1 = OrMap[self.pins["C1"].value][self.pins["C2"].value]
			v2 = OrMap[self.pins["B1"].value][self.pins["B2"].value]
			v3 = OrMap[self.pins["A1"].value][self.pins["A2"].value]
			value = AndMap[v1][v2]
			value = AndMap[value][v3]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("OAI33_"):
			v1 = OrMap[self.pins["B1"].value][self.pins["B2"].value]
			v2 = OrMap[self.pins["B3"]][v1]
			v3 = OrMap[self.pins["A1"].value][self.pins["A2"].value]
			v4 = OrMap[self.pins["A3"]][v3]
			value = AndMap[v2][v4]
			self.pins["ZN"].set_value(NotMap[value])

		elif self.gtype.startswith("MUX"):
			v1 = AndMap[self.pins["A"].value][NotMap[self.pins["S"].value]]
			v2 = AndMap[self.pins["B"].value][self.pins["S"].value]
			self.pins["Z"].set_value(OrMap[v1][v2])

		elif self.gtype.startswith("FA"):
			v1 = XorMap[self.pins["A"].value][self.pins["B"].value]
			self.pins["S"].set_value(XorMap[v1][self.pins["CI"].value])
			v2 = OrMap[self.pins["A"].value][self.pins["B"].value]
			v3 = AndMap[v2][self.pins["CI"].value]
			v4 = AndMap[self.pins["A"].value][self.pins["B"].value]
			self.pins["CO"].set_value(OrMap[v3][v4])

		elif "DFF" in self.gtype:
			self.pins["Q"].set_value(self.pins["D"].value)
			if "QN" in self.pins:
				self.pins["QN"].set_value(NotMap[self.pins["D"].value])

		else:
			self.pins["Z"].set_value(self.pins["A"].value)
		
	 	
class Wire:
	def __init__(self, wtype, name):
		self.wtype = wtype			#Wire type
		self.value = -1					#Signal on this wire
		self.name = name				#Wire name
 		self.fanin = 0					#Fanin gate
		self.fanout = []				#Fanout gates	
	
	def connect(self, gate, direction):
		if direction == "IN":
			self.fanin = gate
		else:
			self.fanout.append(gate)
	
	def set_value(self, v):
		self.value = v

class Circuit:
	def __init__(self):
		self.Pi = {} 						#Primary Input
		self.Po = {}						#Primary Output
		self.Wire = {}					#Wires
		self.Gate = {}					#Standard Cell Gates
		self.sorted_Gate = {}		#Sorted gates by their levels
		self.scanchains = []		#Scanchains
		self.maxlevel = -1			#Maxlevel
	
	def debug(self):
		for g in self.sorted_Gate:
			gate = self.sorted_Gate[g]
			print(gate.gtype + " " +  gate.name + " " + str(gate.level))

	#Verilog Parser
	def parseVerilog(self, infile):
		f = open(infile, "r")
		
		for line in f:
			if ");" in line:
				break

		#Parse Primary Inputs
		for line in f:
			l = line.strip().strip(";")
			wires = l.split(",")
			for w in wires:
				if ("input" in w):
					w = w.replace("input","")
				elif not w:
					continue
				name = w.strip()
				newWire = Wire("PI", name)
				self.Pi[name] = newWire
				self.Wire[name] = newWire
			
			if ";" in line:
				break	

		#Parse Primary Outputs
		for line in f:
			l = line.strip().strip(";")
			wires = l.split(",")
			for w in wires:
				if ("output" in w):
					w = w.replace("output","")
				elif not w:
					continue
				name = w.strip()
				newWire = Wire("PO", name)
				self.Po[name] = newWire
				self.Wire[name] = newWire
			
			if ";" in line:
				break	
			
		#Parse Wires
		for line in f:
			l = line.strip().strip(";")
			wires = l.split(",")
			for w in wires:
				if ("wire " in w):
					w = w.replace("wire ","")
				elif not w:
					continue
				name = w.strip()
				newWire = Wire("WIRE", name)
				self.Wire[name] = newWire
			
			if ";" in line:
				break	
		
		#Direct assign
		for line in f:
			if "assign" not in line:
			 break
			words = line.split()
			inwire = words[3].strip(";")
			outwire = words[1]
			
			gname = "Dummy_" + inwire
			newGate = Gate("Dummy", gname)
			newGate.add_pins("A", self.Wire[inwire])
			self.Wire[inwire].connect(newGate, "OUT")
			newGate.add_pins("Z", self.Wire[outwire])
			self.Wire[inwire].connect(newGate, "IN")
			self.Gate[gname] = newGate
			
		i = 0
		#Parse Gates
		l = ""
		for line in f:
			if not line:
				continue
			elif "endmodule" in line:
				break
			l += line.strip()
			if ";" not in line:
				continue
			
			gtype = l.split()[0]
			name = l.split()[1]
			newGate = Gate(gtype, name)

			pins = l.split(",")
			for p in pins:
				idx1 = p.find(".")
				idx2 = p.find("(", idx1)
				idx3 = p.find(")", idx2)
				
				ptype = p[idx1+1:idx2].strip()
				wire = p[idx2+1:idx3].strip()
				newGate.add_pins(ptype, self.Wire[wire])
				if "Z" in ptype:
					self.Wire[wire].connect(newGate, "IN")
				elif "CO" in ptype:
					self.Wire[wire].connect(newGate, "IN")
				elif "Q" in ptype:
					self.Wire[wire].connect(newGate, "IN")
				elif "S" in ptype:
					self.Wire[wire].connect(newGate, "IN")
					
				else:
					self.Wire[wire].connect(newGate, "OUT")
					

			self.Gate[name] = newGate
			l = ""
		
		f.close()
				
	def levelize(self):
		for p in self.Pi:
			self.levelize_dfs(self.Pi[p], 0)
		for sc in self.scanchains:
			for gate in sc:
				gate.set_level(0)
				self.levelize_dfs(gate.pins["Q"], 1)
				if "QN" in gate.pins:
					self.levelize_dfs(gate.pins["QN"], 1)

		print("Max level:" + str(self.maxlevel))
		
		self.sorted_Gate = [[] for x in range(self.maxlevel+1)]
		for g in self.Gate:
			gate = self.Gate[g]
			l = gate.level
			self.sorted_Gate[l].append(gate)

		
	
	def levelize_dfs(self, wire, level):
		for gate in wire.fanout:
			if "DFF" in gate.gtype:
				continue
			if gate.level < level:
				gate.set_level(level)
				self.maxlevel = max(level, self.maxlevel)
				if "Z" in gate.pins:
					self.levelize_dfs(gate.pins["Z"], level+1)
				if "ZN" in gate.pins:
					self.levelize_dfs(gate.pins["ZN"], level+1)
				if "CO" in gate.pins:
					self.levelize_dfs(gate.pins["CO"], level+1)
				if "S" in gate.pins:
					self.levelize_dfs(gate.pins["S"], level+1)
	
	def parseScanChain(self, infile):
		f = open(infile, "r")
		inchain = False
		chain = []
		for line in f:
			if "PatternBurst" in line:
				break

			if not inchain:
				if "ScanCells" not in line:
					continue

			inchain = True
			for words in line.split("\""):
				if "." not in words:
					continue
				idx1 = words.find(".")+1
				idx2 = words.find(".", idx1+1)
				name = words[idx1:idx2]
				chain.append(self.Gate[name])
			
			if ";" in line:
				inchain = False
				self.scanchains.append(chain)
				chain = []

		f.close()
		self.levelize()


			

cir = Circuit()
cir.parseVerilog(sys.argv[1])
cir.parseScanChain(sys.argv[2])
#cir.debug()

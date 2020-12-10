import sys

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

def evalNot(v):
	return NotMap[v]

def evalAnd(v1, v2):
	return AndMap[v1][v2]

def evalOr(v1, v2):
	return OrMap[v1][v2]

def evalXor(v1, v2):
	return XorMap[v1][v2]



class Gate:
	def __init__(self, gtype, name):
		self.gtype = gtype			#Gate type
	 	self.level = -1					#Level in the circuit
	 	self.name = name				#Gate name
	 	self.pins = {}					#Input/Output pins
		
	def add_pins(self, ptype, wire):
		self.pins[ptype] = wire
	

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
			else 
				self.pins["ZN"].set_value(value)
			
				
		

	 	
class Wire:
	def __init__(self, wtype, name):
		self.wtype = wtype			#Wire type
		self.value = 0					#Signal on this wire
		self.name = name				#Wire name
 		self.fanin = 0					#Fanin gate
		self.fanout = []				#Fanout gates	

class Circuit:
	def __init__(self):
		self.Pi = {} 						#Primary Input
		self.Po = {}						#Primary Output
		self.Wire = {}					#Wires
		self.Gate = {}					#Standard Cell Gates
	
	def debug(self):
		for g in self.Gate:
			gate = self.Gate[g]
			print(gate.gtype + " " +  gate.name + " " + str(len(gate.pins)))

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
			newGate.add_pins("Z", self.Wire[outwire])
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

			self.Gate[name] = newGate
			l = ""
				

cir = Circuit()
cir.parseVerilog(sys.argv[1])
cir.debug()

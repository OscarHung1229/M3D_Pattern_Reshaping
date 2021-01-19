import gurobipy as gp
from gurobipy import GRB


def buildconstr(m,g,ite):
	it = "_"+str(ite)

	if g.gtype.startswith("INV"):
		vA = m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		m.addConstr(vZN == 1-vA)

	elif g.gtype.startswith("AND") or g.gtype.startswith("NAND"):
		l = []
		for p in self.pins:
			if "Z" in p:	
				continue:
			else:
				l.append(m.getVarByName(self.pins[p].name+it))
		
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		
		if "NAND" in self.gtype:
			v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
			m.addGenConstrAnd(v1,l)
			m.addConstr(vZN == 1-v1)
			
		else:
			m.addGenConstrAnd(vZN, l)
			
	elif g.gtype.startswith("OR") or g.gtype.startswith("NOR"):
		l = []
		for p in self.pins:
			if "Z" in p:	
				continue:
			else:
				l.append(m.getVarByName(self.pins[p].name+it))
		
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		
		if "NOR" in self.gtype:
			v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
			m.addGenConstrOr(v1,l)
			m.addConstr(vZN == 1-v1)
			
		else:
			m.addGenConstrOr(vZN, l)

	elif self.gtype.startswith("AOI21_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrAnd(v1, (vB1,vB2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (v1,vA))
		m.addConstr(vZN == 1-v2)

	elif self.gtype.startswith("AOI22_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA1 = m.getVarByName(g.pins["A1"].name+it)
		vA2 = m.getVarByName(g.pins["A2"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrAnd(v1, (vB1,vB2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (vA1,vA2))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrOr(v3, (v1,v2))
		m.addConstr(vZN == 1-v3)

	elif self.gtype.startswith("AOI211_"):
		vC1 = m.getVarByName(g.pins["C1"].name+it)
		vC2 = m.getVarByName(g.pins["C2"].name+it)
		vB = 	 m.getVarByName(g.pins["B"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)
	
		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrAnd(v1, (vC1,vC2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (v1,vB,vA))
		m.addConstr(vZN == 1-v2)

	elif self.gtype.startswith("AOI221_"):
		vC1 = m.getVarByName(g.pins["C1"].name+it)
		vC2 = m.getVarByName(g.pins["C2"].name+it)
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)
	
		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrAnd(v1, (vC1,vC2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (vB1,vB2))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrOr(v3, (v1,v2,vA))
		m.addConstr(vZN == 1-v3)

	elif self.gtype.startswith("AOI222_"):
		vC1 = m.getVarByName(g.pins["C1"].name+it)
		vC2 = m.getVarByName(g.pins["C2"].name+it)
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA1 = m.getVarByName(g.pins["A1"].name+it)
		vA2 = m.getVarByName(g.pins["A2"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrAnd(v1, (vC1,vC2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (vB1,vB2))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (vA1,vA2))
		v4 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v4"+it)
		m.addGenConstOr(v4, (v1,v2,v3))
		m.addConstr(vZN == 1-v4)

	elif self.gtype.startswith("OAI21_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vB1,vB2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (v1,vA))
		m.addConstr(vZN == 1-v2)

	elif self.gtype.startswith("OAI22_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA1 = m.getVarByName(g.pins["A1"].name+it)
		vA2 = m.getVarByName(g.pins["A2"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vB1,vB2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (vA1,vA2))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (v1,v2))
		m.addConstr(vZN == 1-v3)

	elif self.gtype.startswith("OAI211_"):
		vC1 = m.getVarByName(g.pins["C1"].name+it)
		vC2 = m.getVarByName(g.pins["C2"].name+it)
		vB = 	 m.getVarByName(g.pins["B"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vC1,vC2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (v1,vB,vA))
		m.addConstr(vZN == 1-v2)

	elif self.gtype.startswith("OAI222_"):
		vC1 = m.getVarByName(g.pins["C1"].name+it)
		vC2 = m.getVarByName(g.pins["C2"].name+it)
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA1 = m.getVarByName(g.pins["A1"].name+it)
		vA2 = m.getVarByName(g.pins["A2"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vC1,vC2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (vB1,vB2))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrOr(v3, (vA1,vA2))
		v4 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v4"+it)
		m.addGenConstrAnd(v4, (v1,v2,v3))
		m.addConstr(vZN == 1-v4)

	elif self.gtype.startswith("OAI33_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vB3 = m.getVarByName(g.pins["B3"].name+it)
		vA1 = m.getVarByName(g.pins["A1"].name+it)
		vA2 = m.getVarByName(g.pins["A2"].name+it)
		vA3 = m.getVarByName(g.pins["A3"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vB1,vB2,vB3))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (vA1,vA2,vA3))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (v1,v2))
		m.addConstr(vZN == 1-v3)

	elif self.gtype.startswith("MUX"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vS = m.getVarByName(g.pins["S"].name+it)
		vZ = m.getVarByName(g.pins["Z"].name+it)
		
		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addConstr(v1 == 1-vS)
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (v1,vA))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (vB,vS))
		m.addGenConstrOr(vZ, (v1,v2))

	elif self.gtype.startswith("FA"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vS = m.getVarByName(g.pins["S"].name+it)
		vCI = m.getVarByName(g.pins["CI"].name+it)
		vCO = m.getVarByName(g.pins["CO"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrIndicator(v1, True, vA+vB, GRB.EQUAL, 1.0)
		m.addGenConstrIndicator(vS, True, v1+vCI, GRB.EQUAL, 1.0)
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (vA,vB))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (v2,vCI))
		v4 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v4"+it)
		m.addGenConstrAnd(v4, (vA,vB))
		m.addGenConstrOr(vCO, (v3,v4))

	elif self.gtype.startswith("XOR"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vZ = m.getVarByName(g.pins["Z"].name+it)
		m.addGenConstrIndicator(vZ, True, vA+vB, GRB.EQUAL, 1.0)

	elif self.gtype.startswith("XNOR"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		m.addGenConstrIndicator(vZN, False, vA+vB, GRB.EQUAL, 1.0)

	elif self.gtype.startswith("SDFF"):
		if ite == 2:
			vD = m.getVarByName(g.pins["D"].name+"_1")
			vQ = m.getVarByName(g.pins["Q"].name+"_2")
			m.addConstr(vQ == vD)
			if "QN" in g.pins:
				vQN = m.getVarByName(g.pins["QN"].name+"_2")
				m.addConstr(vQN == 1-vD)
	
	else:
		vA = m.getVarByName(g.pins["A"].name+it)
		vZ = m.getVarByName(g.pins["Z"].name+it)
		m.addConstr(vZ == vA)
				
			

def construct(cir):
	try:

  	# Create a new model
		m = gp.Model("TPG")
		obj = 0

		# Create variable for each wire
		for w in self.Wire:
			n1 = w+"_1"
			n2 = w+"_2"
			m.addVar(vtype=GRB.BINARY, name=n1)
			m.addVar(vtype=GRB.BINARY, name=n2)

		# Add constraint for each wire
		for w in self.Wire:
			wire = self.Wire[w]
			g = wire.fanin
			n1 = w+"_1"
			v1 = m.getVarByName(n1)
			n2 = w+"_2"
			v2 = m.getVarByName(n2)

			if g == 0:
				if wire.v1 != 2:
					m.addConstr(v1 == wire.v1)
				if wire.v2 != 2:
					m.addConstr(v2 == wire.v2)
				continue

					
			if wire.v1 == 2:
				buildconstr(m,g,1)
			else:
				m.addConstr(v1 == wire.v1)

			if w.v2 == 2:
				buildconstr(m,g,2)
			else:
				m.addConstr(v2 == wire.v2)

			if g.die == 0:
				sw = m.addVar(vtype=GRB.BINARY, name=g.name+"_sw")
				m.addConstrIndicator(sw, True, v1+v2, GRB.EQUAL, 1.0)
				obj += len(w.fanout)*sw
				

		# Set objective
		m.setObjective(obj, GRB.MINIMIZE)

		# Optimize model
		m.optimize()
	
		#for v in m.getVars():
		#	print('%s %g' % (v.varName, v.x))
	
		print('Obj: %g' % m.objVal)
	
	except gp.GurobiError as e:
		print('Error code ' + str(e.errno) + ': ' + str(e))
	
	except AttributeError:
		print('Encountered an attribute error')

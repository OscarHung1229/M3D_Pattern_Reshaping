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
		for p in g.pins:
			if "Z" in p:	
				continue
			else:
				l.append(m.getVarByName(g.pins[p].name+it))
		
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		
		if "NAND" in g.gtype:
			v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
			m.addGenConstrAnd(v1,l)
			m.addConstr(vZN == 1-v1)
			
		else:
			m.addGenConstrAnd(vZN, l)
			
	elif g.gtype.startswith("OR") or g.gtype.startswith("NOR"):
		l = []
		for p in g.pins:
			if "Z" in p:	
				continue
			else:
				l.append(m.getVarByName(g.pins[p].name+it))
		
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		
		if "NOR" in g.gtype:
			v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
			m.addGenConstrOr(v1,l)
			m.addConstr(vZN == 1-v1)
			
		else:
			m.addGenConstrOr(vZN, l)

	elif g.gtype.startswith("AOI21_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrAnd(v1, (vB1,vB2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (v1,vA))
		m.addConstr(vZN == 1-v2)

	elif g.gtype.startswith("AOI22_"):
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

	elif g.gtype.startswith("AOI211_"):
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

	elif g.gtype.startswith("AOI221_"):
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

	elif g.gtype.startswith("AOI222_"):
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
		m.addGenConstrOr(v4, (v1,v2,v3))
		m.addConstr(vZN == 1-v4)

	elif g.gtype.startswith("OAI21_"):
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vB1,vB2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrAnd(v2, (v1,vA))
		m.addConstr(vZN == 1-v2)

	elif g.gtype.startswith("OAI22_"):
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

	elif g.gtype.startswith("OAI211_"):
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

	elif g.gtype.startswith("OAI221_"):
		vC1 = m.getVarByName(g.pins["C1"].name+it)
		vC2 = m.getVarByName(g.pins["C2"].name+it)
		vB1 = m.getVarByName(g.pins["B1"].name+it)
		vB2 = m.getVarByName(g.pins["B2"].name+it)
		vA = 	 m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)
	
		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addGenConstrOr(v1, (vC1,vC2))
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (vB1,vB2))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (v1,v2,vA))
		m.addConstr(vZN == 1-v3)

	elif g.gtype.startswith("OAI222_"):
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

	elif g.gtype.startswith("OAI33_"):
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

	elif g.gtype.startswith("MUX"):
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

	elif g.gtype.startswith("FA"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vS = m.getVarByName(g.pins["S"].name+it)
		vCI = m.getVarByName(g.pins["CI"].name+it)
		vCO = m.getVarByName(g.pins["CO"].name+it)

		v1 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v1"+it)
		m.addConstr(v1-vA-vB <= 0)
		m.addConstr(v1-vA+vB >= 0)
		m.addConstr(v1+vA-vB >= 0)
		m.addConstr(v1+vA+vB <= 2)
		m.addConstr(vS-v1-vCI <= 0)
		m.addConstr(vS-v1+vCI >= 0)
		m.addConstr(vS+v1-vCI >= 0)
		m.addConstr(vS+v1+vCI <= 2)
		v2 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v2"+it)
		m.addGenConstrOr(v2, (vA,vB))
		v3 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v3"+it)
		m.addGenConstrAnd(v3, (v2,vCI))
		v4 = m.addVar(vtype=GRB.BINARY, name=g.name+"_v4"+it)
		m.addGenConstrAnd(v4, (vA,vB))
		m.addGenConstrOr(vCO, (v3,v4))

	elif g.gtype.startswith("XOR"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vZ = m.getVarByName(g.pins["Z"].name+it)
		m.addConstr(vZ-vA-vB <= 0)
		m.addConstr(vZ-vA+vB >= 0)
		m.addConstr(vZ+vA-vB >= 0)
		m.addConstr(vZ+vA+vB <= 2)

	elif g.gtype.startswith("XNOR"):
		vB = m.getVarByName(g.pins["B"].name+it)
		vA = m.getVarByName(g.pins["A"].name+it)
		vZN = m.getVarByName(g.pins["ZN"].name+it)
		m.addConstr(1-vZN-vA-vB <= 0)
		m.addConstr(1-vZN-vA+vB >= 0)
		m.addConstr(1-vZN+vA-vB >= 0)
		m.addConstr(1-vZN+vA+vB <= 2)

	elif g.gtype.startswith("SDFF"):
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
	#try:

  	# Create a new model
		m = gp.Model("TPG")
		obj = 0

		# Create variable for each wire
		for w in cir.Wire:
			n1 = w+"_1"
			n2 = w+"_2"
			m.addVar(vtype=GRB.BINARY, name=n1)
			m.addVar(vtype=GRB.BINARY, name=n2)

		m.update()

		# Add constraint for each wire
		for w in cir.Wire:
			wire = cir.Wire[w]
			g = wire.fanin
			n1 = w+"_1"
			var1 = m.getVarByName(n1)
			n2 = w+"_2"
			var2 = m.getVarByName(n2)

			if g == 0:
				if wire.v1 != 2 and wire.v1 != 99:
					m.addConstr(var1 == wire.v1)
				if wire.v2 != 2 and wire.v2 != 99:
					m.addConstr(var2 == wire.v2)
				continue

			if wire.v1 == 2:
				buildconstr(m,g,1)
			elif wire.v1 == 1 or wire.v1 == 3:
				m.addConstr(var1 == 1)
			else:
				m.addConstr(var1 == 0)

			if wire.v2 == 2:
				buildconstr(m,g,2)
			elif wire.v2 == 1 or wire.v2 == 3:
				m.addConstr(var2 == 1)
			else:
				m.addConstr(var2 == 0)



			if g.die == 0:
				sw = m.addVar(vtype=GRB.BINARY, name=g.name+"_sw")
				m.addConstr(sw-var1-var2 <= 0)
				m.addConstr(sw-var1+var2 >= 0)
				m.addConstr(sw+var1-var2 >= 0)
				m.addConstr(sw+var1+var2 <= 2)
				obj += len(wire.fanout)*sw
				
		print("Finish wire constraints")

		# Set objective
		m.setObjective(obj, GRB.MINIMIZE)

		# Set parameters
		m.setParam('MIPGap', 0.005)
		m.setParam('TimeLimit', 3600)
		m.setParam(GRB.Param.Threads, 10)

		# Optimize model
		m.optimize()
		
		if (m.status == GRB.OPTIMAL):
			dict1 = {}
			for wire in cir.Pi:
				if wire.v1 == 2:
					name = wire.name+"_1"
					var = m.getVarByName(name)
					dict1[wire.name] = int(var.x)
				else:
					dict1[wire.name] = wire.v1
				
				if wire.v2 != 2 and wire.v2 != wire.v1:
					dict1[wire.name+"_v2"] = wire.v2

			for chain in cir.scanchains:
				for g in chain:
					wire = g.pins["Q"]
					if wire.v1 == 2:
						name = wire.name+"_1"
						var = m.getVarByName(name)
						dict1[wire.name] = int(var.x)
					else:
						dict1[wire.name] = wire.v1
			
			cir.ilppat.append(dict1)
			print('Obj: %g' % m.objVal)
			return True
		else:
			return False
					

	
		#for v in m.getVars():
		#	print('%s %g' % (v.varName, v.x))
	
		print('Obj: %g' % m.objVal)
	
	#except gp.GurobiError as e:
	#	print('Error code ' + str(e.errno) + ': ' + str(e))
	#	m.computeIIS()
	#	m.write("model.ilp")
	#	#return False
	
	#except AttributeError:
	#	print('Encountered an attribute error')
	#	#return False

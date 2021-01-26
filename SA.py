import random
from math import exp
from random import randint

def probAnd(v1,v2):
	return v1*v2
def probOr(v1,v2):
	return v1 + (1-v1)*v2
def probXor(v1,v2):
	return v1*(1-v2)+v2*(1-v1)

def calProb(g):
	if g.gtype.startswith("INV"):
		vA = g.pins["A"].prob
		g.pins["ZN"].prob = 1-vA

	elif g.gtype.startswith("AND") or g.gtype.startswith("NAND"):
		pr = 1
		for p in g.pins:
			if "Z" in p:	
				continue
			else:
				pr = probAnd(pr, g.pins[p].prob)
		
		if "NAND" in g.gtype:
			g.pins["ZN"].prob = 1-pr
			
		else:
			g.pins["ZN"].prob = pr
			
	elif g.gtype.startswith("OR") or g.gtype.startswith("NOR"):
		pr = 0
		for p in g.pins:
			if "Z" in p:	
				continue
			else:
				pr = probOr(pr, g.pins[p].prob)
				
		
		vZN = g.pins["ZN"].prob
		
		if "NOR" in g.gtype:
			g.pins["ZN"].prob = 1-pr
			
		else:
			g.pins["ZN"].prob = pr

	elif g.gtype.startswith("AOI21_"):
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA = 	 g.pins["A"].prob

		pr = probOr(probAnd(vB1,vB2), vA)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("AOI22_"):
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA1 = g.pins["A1"].prob
		vA2 = g.pins["A2"].prob

		pr = probOr(probAnd(vB1,vB2), probAnd(vA1,vA2))
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("AOI211_"):
		vC1 = g.pins["C1"].prob
		vC2 = g.pins["C2"].prob
		vB = 	 g.pins["B"].prob
		vA = 	 g.pins["A"].prob
	
		pr = probAnd(vC1,vC2)
		pr = probOr(pr,vB)
		pr = probOr(pr,vA)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("AOI221_"):
		vC1 = g.pins["C1"].prob
		vC2 = g.pins["C2"].prob
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA = 	 g.pins["A"].prob
	
		pr = probOr(probAnd(vC1,vC2), probAnd(vB1,vB2))
		pr = probOr(pr, vA)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("AOI222_"):
		vC1 = g.pins["C1"].prob
		vC2 = g.pins["C2"].prob
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA1 = g.pins["A1"].prob
		vA2 = g.pins["A2"].prob

		pr = probOr(probAnd(vC1,vC2), probAnd(vB1,vB2))
		pr = probOr(pr, probAnd(vA1,vA2))
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("OAI21_"):
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA = 	 g.pins["A"].prob

		pr = probAnd(probOr(vB1,vB2), vA)
		g.pins["ZN"].prob = 1-pr


	elif g.gtype.startswith("OAI22_"):
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA1 = g.pins["A1"].prob
		vA2 = g.pins["A2"].prob

		pr1 = probOr(vB1,vB2)
		pr2 = probOr(vA1,vA2)
		pr = probAnd(pr1, pr2)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("OAI211_"):
		vC1 = g.pins["C1"].prob
		vC2 = g.pins["C2"].prob
		vB = 	 g.pins["B"].prob
		vA = 	 g.pins["A"].prob

		pr = probOr(vC1, vC2)
		pr = probAnd(pr, vB)
		pr = probAnd(pr, vA)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("OAI221_"):
		vC1 = g.pins["C1"].prob
		vC2 = g.pins["C2"].prob
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA = 	 g.pins["A"].prob
	
		pr = probAnd(probOr(vC1, vC2), probOr(vB1,vB2))
		pr = probAnd(pr, vA)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("OAI222_"):
		vC1 = g.pins["C1"].prob
		vC2 = g.pins["C2"].prob
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vA1 = g.pins["A1"].prob
		vA2 = g.pins["A2"].prob

		pr = probAnd(probOr(vC1, vC2), probOr(vB1,vB2))
		pr = probAnd(pr, probOr(vA1,vA2))
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("OAI33_"):
		vB1 = g.pins["B1"].prob
		vB2 = g.pins["B2"].prob
		vB3 = g.pins["B3"].prob
		vA1 = g.pins["A1"].prob
		vA2 = g.pins["A2"].prob
		vA3 = g.pins["A3"].prob

		pr1 = probOr(vB3, probOr(vB1,vB2))
		pr2 = probOr(vA3, probOr(vA1,vA2))
		pr = probAnd(pr1, pr2)
		g.pins["ZN"].prob = 1-pr
		
	elif g.gtype.startswith("MUX"):
		vB = g.pins["B"].prob
		vA = g.pins["A"].prob
		vS = g.pins["S"].prob
		vZ = g.pins["Z"].prob
		
		pr1 = probAnd(vA, 1-vS)
		pr2 = probAnd(vB, vS)
		pr = probOr(pr1, pr2)
		g.pins["Z"].prob = pr
		
	elif g.gtype.startswith("FA"):
		vB = g.pins["B"].prob
		vA = g.pins["A"].prob
		vCI = g.pins["CI"].prob

		pr1 = probXor(vA, vB)
		pr1 = probXor(vCI, pr1)
		g.pins["S"].prob = pr1
		pr2 = probAnd(probOr(vA,vB), vCI)
		pr3 = probAnd(vA,vB)
		pr3 = probOr(pr2, pr3)
		g.pins["CO"].prob = pr3
		
	elif g.gtype.startswith("XOR"):
		vB = g.pins["B"].prob
		vA = g.pins["A"].prob

		pr = probXor(vB,vA)
		g.pins["Z"].prob = pr

	elif g.gtype.startswith("XNOR"):
		vB = g.pins["B"].prob
		vA = g.pins["A"].prob
		vZN = g.pins["ZN"].prob

		pr = probXor(vB,vA)
		g.pins["ZN"].prob = 1-pr

	elif g.gtype.startswith("SDFF"):
		assert(False)
	
	else:
		vA = g.pins["A"].prob
		g.pins["Z"].prob = vA
				


class Minimize:
	def __init__(self, cir, step_max=50, t_min=0, t_max=100, alpha=0.8):
		self.cir = cir
		self.design = cir.design
		self.t = t_max
		self.t_max = t_max
		self.t_min = t_min
		self.step = 1
		self.accept = 0
		self.step_max = step_max
		self.current_state = {}
		self.current_energy = 0
		self.best_state = self.current_state
		self.best_energy = self.current_energy
		self.free_var = []

	def initstate(self):
		for i in range(len(self.cir.sorted_Gate)):
			if i == 0:
				continue
			gates = self.cir.sorted_Gate[i]	
			for g in gates:
				calProb(g)

		dict1 = {}
		for pi in self.cir.Pi:
			if pi.value == 2:
				self.free_var.append(pi.name)
				v = randint(0, 1)
				dict1[pi.name] = v
			else:
				dict1[pi.name] = pi.v1
			
			if self.cir.design == "ldpc":
				if pi.v2 != 2:
					name = pi.name + "_v2"
					dict1[name] = pi.v2
			

		for chain in self.cir.scanchains:
			for cell in chain:
				p = cell.pins["Q"]
				if p.value == 2:
					self.free_var.append(p.name)
					v = randint(0, 1)
					if cell.pins["D"].prob > 0.5:
						v = 1
					elif cell.pins["D"].prob < 0.5:
						v = 0
					dict1[p.name] = v
				else:
					dict1[p.name] = p.v1


		return dict1

	def cost_func(self, dict1):
		for pi in self.cir.Pi:
			if pi.name in dict1:
				pi.set_value(dict1[pi.name], True)
			else:
				pi.set_value(pi.v1, True)

		for chain in self.cir.scanchains:
			for cell in chain:
				p = cell.pins["Q"]
				if p.name in dict1:
					p.set_value(dict1[p.name], True)
					if "QN" in cell.pins:
						cell.pins["QN"].set_value(1-dict1[p.name], True)
				else:
					p.set_value(p.v1, True)
					if "QN" in cell.pins:
						cell.pins["QN"].set_value(1-p.v1, True)
			
		self.cir.evaluate(True)
		cost = self.cir.evaluate(False)

		return cost
	
	def get_neighbor(self):
		key = random.sample(self.free_var,1)[0]
		dict1 = self.current_state.copy()
		dict1[key] = 1-dict1[key]
		return dict1

	def main(self):
		self.current_state = self.initstate()
		self.current_energy = self.cost_func(self.current_state)
		self.best_state = self.current_state
		self.best_energy = self.current_energy
		init_energy = self.current_energy
	
		self.cir.preferpat.append(self.best_state)	
	
		while self.step < self.step_max and self.t >= self.t_min:

			# get neighbor
			newdict = self.get_neighbor()	
			
			# check energy level of neighbor
 			E_n = self.cost_func(newdict)
			dE = E_n - self.current_energy

			if random.random() < exp(-dE/self.t):	
				self.current_energy = E_n
				self.current_state = newdict
				self.accept += 1

			if E_n < self.best_energy:
				self.best_energy = E_n
				self.best_state = newdict

			self.t -= self.t_max/self.step_max
			self.step += 1


		self.cir.reshapepat.append(self.best_state)	
		print("\nInitial energy: {0}, Best energy: {1}, Minimize: {2}, Acceptance rate: {3:.2f}".format(init_energy, self.best_energy, (init_energy>self.best_energy), float(self.accept)/float(self.step)))
		filename = self.design + "/SA.rpt"
		with open(filename, 'a') as fout:
			fout.write("Initial energy: {0}, Best energy: {1}, Minimize: {2}, Acceptance rate: {3:.2f}\n".format(init_energy, self.best_energy, (init_energy>self.best_energy), float(self.accept)/float(self.step)))
			

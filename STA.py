def dumpSTA(cir, prefer, pat, SDD):
	prefix = ""
	if cir.design == "ldpc":
		prefix = "/autofs/home/sh528/ldpc_tight/"
	elif cir.design == "tate":
		prefix = "/autofs/home/sh528/ITC2020/tate_1G_forTest/"
	elif cir.design == "netcard":
		prefix = "/autofs/home/sh528/ITC2020/netcard_v4/"
	elif cir.design == "leon3":
		prefix = "/autofs/home/sh528/ITC2020/leon_v3/"
	else:
		print("Design " + cir.design + " not exists!")
		assert(False)

	filename = "/autofs/home/sh528/M3D_Pattern_Reshaping/" + cir.design + "/" + cir.design + "_"
	report = ""
	if prefer:
		filename += "sta_prefer" + SDD + ".tcl"
		report = "/autofs/home/sh528/M3D_Pattern_Reshaping/" + cir.design + "/prefer_timing" + SDD + ".rpt"
	else:
		filename += "sta_reshape" + SDD + ".tcl"
		report = "/autofs/home/sh528/M3D_Pattern_Reshaping/" + cir.design + "/reshape_timing" + SDD + ".rpt"
		

	if pat==1:
		with open(filename, "w") as f:
			f.write("\nset target_library \"/autofs/home/sh528/nangate45nm/2d_db/NG45nm_tt_ecsm.db\"\n")
			f.write("set link_library \"* $target_library\"\n")
			f.write("read_verilog " + prefix +  "die0.v\n")
			f.write("read_verilog " + prefix +  "die1.v\n")
			f.write("read_verilog " + prefix +  "top.v\n")
			f.write("current_design top\n")
			f.write("link\n")	
			f.write("source " + prefix + cir.design + ".sdc\n")
		 	f.write("read_parasitic " + prefix + "top.spef\n")	
			f.write("read_parasitic " + prefix + "die0_noOpt.spef -path Udie0\n")
			f.write("read_parasitic " + prefix + "die1_noOpt.spef -path Udie1\n")
	
	with open(filename, "a\n") as f:
		f.write("# Pattern" + str(pat) + "\n")
		f.write("remove_case_analysis -all\n")


	zero = "set_case_analysis 0 {"
	one = "set_case_analysis 1 {"
	rising = "set_case_analysis rising {"
	falling = "set_case_analysis falling {"
	
	for w in cir.Pi:
		if w.name == "clock" or w.name == "clk" or w.name == "ispd_clk":
			rising += w.name + " "
			continue
		elif w.name == "test_se":
			zero += w.name + " "
			continue

		if w.v2 == 0:
			zero += w.name + " "
		elif w.v2 == 1:
			one += w.name + " "
		else:
			assert(False)
		
	for chain in cir.scanchains:
		for cell in chain:
			if cell.pins["Q"].v2 == 0:
				zero += "Udie" + str(cell.die) + "/" + cell.name + "/Q "
				if "QN" in cell.pins:
					one += "Udie" + str(cell.die) + "/" + cell.name + "/QN "
			elif cell.pins["Q"].v2 == 1:
				one += "Udie" + str(cell.die) + "/" + cell.name + "/Q "
				if "QN" in cell.pins:
					zero += "Udie" + str(cell.die) + "/" + cell.name + "/QN "
			elif cell.pins["Q"].v2 == 3:
				rising += "Udie" + str(cell.die) + "/" + cell.name + "/Q "
				if "QN" in cell.pins:
					falling += "Udie" + str(cell.die) + "/" + cell.name + "/QN "
			elif cell.pins["Q"].v2 == 4:
				falling += "Udie" + str(cell.die) + "/" + cell.name + "/Q "
				if "QN" in cell.pins:
					rising += "Udie" + str(cell.die) + "/" + cell.name + "/QN "
			else:
				assert(False)

	with open(filename, "a") as f:
		f.write(zero + "}\n")
		f.write(one + "}\n")
		f.write(rising + "}\n")
		f.write(falling + "}\n")

		if pat==1:
			f.write("report_timing -significant_digits 4 > " + report + "\n")
		else:
			f.write("redirect -append " + report + " {report_timing -significant_digits 4}\n")

		

	



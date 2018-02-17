from utility import *
import collections
import itertools

def naked_single(cells_status):
	print("=================== [Naked_Single] ===================")
	#assignment_list = [elem[0] for elem in cells_status.values()]
	#idx_list = [index for index, value in enumerate(assignment_list) if value == 0]
	#for idx in idx_list:
	#	print(idx)
	candidate_values = [elem[1] for elem in cells_status.values()]
	remain_num = [len(x) for x in candidate_values]
	idx_list = [index for index, value in enumerate(remain_num) if value == 1]
	print("* Change cell", idx_list)
	for cell_idx in idx_list:
		print("* Previous", cells_status[cell_idx])
		cells_status[cell_idx][0] = cells_status[cell_idx][1][0]
		cells_status[cell_idx][1] = []
		print("* After", cells_status[cell_idx])

def hidden_single(cells_status):
	print("=================== [Hidden_Single] ===================")
	for i in range(0,10):
		slot_idx = [i] + col_cells(i)
		remove_hidden_single(cells_status, slot_idx)
		slot_idx = [i] + row_cells(i)
		remove_hidden_single(cells_status,slot_idx)
		slot_idx = [i] + box_cells(i)
		remove_hidden_single(cells_status, slot_idx)

def remove_hidden_single(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	counter = collections.Counter(flat_list)
	counter_values = collections.Counter(flat_list).values()
	counter_keys = collections.Counter(flat_list).keys()
	counter_idx_list = [index for index, value in enumerate(counter_values) if value == 1]
	if len(counter_idx_list) > 0:
		count_idx = counter_idx_list[0]
		value = counter_keys[count_idx]
		i = 0
		for sublist in domain_col:
			if value in sublist:
				cell_idx = slot_idx[i]
				print("* Change cell", cell_idx)
				print("domain_col", domain_col)
				print("counter", counter)
				print("* Previous", cells_status[cell_idx])
				cells_status[cell_idx][0] = value
				cells_status[cell_idx][1] = []
				print("* After", cells_status[cell_idx])
				break
			i = i + 1

def naked_pairs(cells_status):
	print("=================== [Naked_Pairs] ===================")
	for i in range(0,10):
		slot_idx = [i] + col_cells(i)
		remove_naked_pairs(cells_status, slot_idx)
		slot_idx = [i] + row_cells(i)
		remove_naked_pairs(cells_status,slot_idx)
		slot_idx = [i] + box_cells(i)
		remove_naked_pairs(cells_status, slot_idx)

def remove_naked_pairs(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	dupes = [x for n, x in enumerate(domain_col) if x in domain_col[:n]]
	pair = [value for index, value in enumerate(dupes) if len(value) == 2]
	if (len(pair) > 0):
		for cell_idx in slot_idx:
			if(len(cells_status[cell_idx][1]) > 0 and cells_status[cell_idx][1] != pair[0]):
				if (pair[0][0] in cells_status[cell_idx][1]):
					print("* Change cell", cell_idx)
					print("domain_col", domain_col)
					print("pair", pair)
					print("* Previous", cells_status[cell_idx])
					cells_status[cell_idx][1].remove(pair[0][0])
					print("* After", cells_status[cell_idx])
				if (pair[0][1] in cells_status[cell_idx][1]):
					print("* Change cell", cell_idx)
					print("domain_col", domain_col)
					print("pair", pair)
					print("* Previous", cells_status[cell_idx])
					cells_status[cell_idx][1].remove(pair[0][1])
					print("* After", cells_status[cell_idx])

def hidden_pairs(cells_status):
	print("=================== [Hidden_Pairs] ===================")
	for i in range(0,10):
		slot_idx = [i] + col_cells(i)
		remove_hidden_pairs(cells_status, slot_idx)
		slot_idx = [i] + row_cells(i)
		remove_hidden_pairs(cells_status,slot_idx)
		slot_idx = [i] + box_cells(i)
		remove_hidden_pairs(cells_status, slot_idx)

def remove_hidden_pairs(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	counter_freq = collections.Counter(flat_list)
	counter_freq_values = collections.Counter(flat_list).values()
	counter_freq_keys = collections.Counter(flat_list).keys()
	counter_freq_idx = [index for index, value in enumerate(counter_freq_values) if value == 1]

	pair_list = []
	for i in domain_col:
		for pair in itertools.combinations(i, 2):
			pair_list.append(pair)

	counter_pair = collections.Counter(pair_list)
	counter_pair_values = collections.Counter(pair_list).values()
	counter_pair_keys = collections.Counter(pair_list).keys()
	counter_pair_idx = [index for index, value in enumerate(counter_pair_values) if value == 2]

	for counter_idx in counter_pair_idx:
		pair = counter_pair_keys[counter_idx]
		if (counter_freq[pair[0]] == 2 and counter_freq[pair[1]] == 2):
			cell_idx = [slot_idx[index] for index, value in enumerate(domain_col) if len(set(value) & set(pair)) == 2]
			for idx in cell_idx:
				print("* Change cell", idx)
				print("domain_col", domain_col)
				print("pair", pair)
				print("* Previous", cells_status[idx])
				cells_status[idx][1] = list(pair)
				print("* After", cells_status[idx])
			break

def naked_triples(cells_status):
	print("=================== [Naked_Triples] =================== ")
	for i in range(0,10):
		slot_idx = [i] + col_cells(i)
		remove_naked_triples(cells_status, slot_idx)
		slot_idx = [i] + row_cells(i)
		remove_naked_triples(cells_status,slot_idx)
		slot_idx = [i] + box_cells(i)
		remove_naked_triples(cells_status, slot_idx)

def remove_naked_triples(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	#print("domain_col", domain_col)
	flat_list = [item for sublist in domain_col for item in sublist]
	triple_list = list(itertools.combinations(set(flat_list), 3))
	#print("triple_list", triple_list)
	for triple in triple_list:
		#print("triple", triple)
		cell_idx = [slot_idx[index] for index, value in enumerate(domain_col)
								if 	len(value) > 0 and
									len(set(triple) & set(value)) > 0 and
									len(set(value) - set(triple)) == 0]
		if len(cell_idx) == 3:
			#print("domain_col", domain_col)
			for idx in slot_idx:
				#print("idx", idx)
				if idx not in cell_idx:
					if triple[0] in cells_status[idx][1]:
						print("* Change cell", idx)
						print("domain_col", domain_col)
						print("triple", triple)
						print("* Previous", cells_status[idx])
						cells_status[idx][1].remove(triple[0])
						print("* After", cells_status[idx])
					if triple[1] in cells_status[idx][1]:
						print("* Change cell", idx)
						print("domain_col", domain_col)
						print("triple", triple)
						print("* Previous", cells_status[idx])
						cells_status[idx][1].remove(triple[1])
						print("* After", cells_status[idx])
					if triple[2] in cells_status[idx][1]:
						print("* Change cell", idx)
						print("domain_col", domain_col)
						print("triple", triple)
						print("* Previous", cells_status[idx])
						cells_status[idx][1].remove(triple[2])
						print("* After", cells_status[idx])
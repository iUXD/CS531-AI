from utility import *
import collections
import itertools

def naked_single(cells_status):
	print(" [Naked_Single] ==============================================")
	#assignment_list = [elem[0] for elem in cells_status.values()]
	#idx_list = [index for index, value in enumerate(assignment_list) if value == 0]
	#for idx in idx_list:
	#	print(idx)
	candidate_values = [elem[1] for elem in cells_status.values()]
	remain_num = [len(x) for x in candidate_values]
	idx_list = [index for index, value in enumerate(remain_num) if value == 1]
	print("*******")
	print(idx_list)
	print("*******")
	for cell_idx in idx_list:
		print(cells_status[cell_idx])
		cells_status[cell_idx][0] = cells_status[cell_idx][1][0]
		cells_status[cell_idx][1] = []
		print(cells_status[cell_idx])

def hidden_single(cells_status):
	print("[Hidden_Single] ==============================================")
	for i in range(0,10):
		slot_idx = [i] + col_cells(i)
		remove_hidden_single(cells_status, slot_idx)
		slot_idx = [i] + row_cells(i)
		remove_hidden_single(cells_status,slot_idx)
		slot_idx = [i] + box_cells(i)
		remove_hidden_single(cells_status, slot_idx)

def remove_hidden_single(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	#print(slot_idx)
	#print([cells_status[x] for x in slot_idx])
	flat_list = [item for sublist in domain_col for item in sublist]
	counter = collections.Counter(flat_list)
	#print(counter)
	counter_values = collections.Counter(flat_list).values()
	counter_keys = collections.Counter(flat_list).keys()
	counter_idx_list = [index for index, value in enumerate(counter_values) if value == 1]
	#for count_idx in counter_idx_list:
	if len(counter_idx_list) > 0:
		count_idx = counter_idx_list[0]
		value = counter_keys[count_idx]
		i = 0
		for sublist in domain_col:
			if value in sublist:
				cell_idx = slot_idx[i]
				print("******************* change cell ", cell_idx)
				print("domains", [cells_status[x] for x in slot_idx])
				print("counter", counter)
				print("previous", cells_status[cell_idx])
				cells_status[cell_idx][0] = value
				cells_status[cell_idx][1] = []
				print("after", cells_status[cell_idx])
				break
			i = i + 1

def naked_pairs(cells_status):
	print(" [Naked_Pairs] ==============================================")
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
		print("pair", pair)
		for cell_idx in slot_idx:
			if(len(cells_status[cell_idx][1]) > 0 and cells_status[cell_idx][1] != pair[0]):
				if (pair[0][0] in cells_status[cell_idx][1]):
					print("previous", cells_status[cell_idx])
					cells_status[cell_idx][1].remove(pair[0][0])
					print("after", cells_status[cell_idx])
				if (pair[0][1] in cells_status[cell_idx][1]):
					print("previous", cells_status[cell_idx])
					cells_status[cell_idx][1].remove(pair[0][1])
					print("after", cells_status[cell_idx])

def hidden_pairs(cells_status):
	print(" [Hidden_Pairs] ==============================================")
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
			print("both are 2s")
			print("domain_col", domain_col)
			print("pair", pair)
			cell_idx = [slot_idx[index] for index, value in enumerate(domain_col) if len(set(value) & set(pair)) == 2]
			for idx in cell_idx:
				print("previous", cells_status[idx])
				cells_status[idx][1] = list(pair)
				print("after", cells_status[idx])
			break
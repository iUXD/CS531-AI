from utility import *
import collections
import itertools

def naked_single(cells_status):
	print("=================== [Naked_Single] ===================")
	candidate_values = [elem[1] for elem in cells_status.values()]
	remain_num = [len(x) for x in candidate_values]
	idx_list = [index for index, value in enumerate(remain_num) if value == 1]
	print("* Change cell", idx_list)
	changed = False
	for cell_idx in idx_list:
		print("* Previous", cells_status[cell_idx])
		cells_status[cell_idx][0] = cells_status[cell_idx][1][0]
		cells_status[cell_idx][1] = []
		print("* After", cells_status[cell_idx])
		changed = True

	return changed

def inference(cells_status, rule_id):
	if rule_id == 11:
		return naked_single(cells_status)
	else:
		changed = False
		for i in range(0,10):
			slot_idx = [i] + col_cells(i)
			changed = changed or inference_slots(cells_status, rule_id, slot_idx)
			slot_idx = [i] + row_cells(i)
			changed = changed or inference_slots(cells_status,rule_id, slot_idx)
			slot_idx = [i] + box_cells(i)
			changed = changed or inference_slots(cells_status, rule_id, slot_idx)
		return changed

def inference_slots(cells_status, rule_id, slot_idx):
	if rule_id == 12:
		return hidden_single(cells_status, slot_idx)
	elif rule_id == 21:
		return naked_pairs(cells_status, slot_idx)
	elif rule_id == 22:
		return hidden_pairs(cells_status, slot_idx)
	elif rule_id == 31:
		return naked_triples(cells_status, slot_idx)
	elif rule_id == 32:
		return hidden_triples(cells_status, slot_idx)
	else:
		print("Wrong rule_id!")
		exit(0)

def hidden_single(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	counter = collections.Counter(flat_list)
	counter_values = collections.Counter(flat_list).values()
	counter_keys = collections.Counter(flat_list).keys()
	counter_idx_list = [index for index, value in enumerate(counter_values) if value == 1]
	changed = False
	if len(counter_idx_list) > 0:
		count_idx = counter_idx_list[0]
		value = counter_keys[count_idx]
		i = 0
		for sublist in domain_col:
			if value in sublist:
				cell_idx = slot_idx[i]
				print("=================== [Hidden_Single] ===================")
				print("* Change cell", cell_idx)
				print("domain_col", domain_col)
				print("counter", counter)
				print("* Previous", cells_status[cell_idx])
				cells_status[cell_idx][0] = value
				cells_status[cell_idx][1] = []
				print("* After", cells_status[cell_idx])
				changed = True
				#break
				return changed
			i = i + 1

def naked_pairs(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	dupes = [x for n, x in enumerate(domain_col) if x in domain_col[:n]]
	pair = [value for index, value in enumerate(dupes) if len(value) == 2]
	changed = False
	if (len(pair) > 0):
		for cell_idx in slot_idx:
			if(len(cells_status[cell_idx][1]) > 0 and cells_status[cell_idx][1] != pair[0]):
				common_values = set(cells_status[cell_idx][1]) & set(pair[0])
				if len(common_values) > 0:
					print("=================== [Naked_Pairs] ===================")
					print("* Change cell", cell_idx)
					print("domain_col", domain_col)
					print("pair", pair)
					print("* Previous", cells_status[cell_idx])
					cells_status[cell_idx][1] = list(set(cells_status[cell_idx][1]) - set(common_values))
					print("* After", cells_status[cell_idx])
					changed = True
	return changed

def hidden_pairs(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	counter_freq = collections.Counter(flat_list)
	counter_freq_values = collections.Counter(flat_list).values()
	counter_freq_keys = collections.Counter(flat_list).keys()
	counter_freq_idx = [index for index, value in enumerate(counter_freq_values) if value == 1]
	changed = False

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
				print("=================== [Hidden_Pairs] ===================")
				print("* Change cell", idx)
				print("domain_col", domain_col)
				print("pair", pair)
				print("* Previous", cells_status[idx])
				cells_status[idx][1] = list(pair)
				print("* After", cells_status[idx])
				changed = True
			#break
			return changed

def naked_triples(cells_status, slot_idx):
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	triple_list = list(itertools.combinations(set(flat_list), 3))
	changed = False

	for triple in triple_list:
		cell_idx = [slot_idx[index] for index, value in enumerate(domain_col)
								if 	len(value) > 0 and
									len(set(triple) & set(value)) > 0 and
									len(set(value) - set(triple)) == 0]

		remain_cell_idx = set(slot_idx) - set(cell_idx)
		if len(cell_idx) == 3:
			for idx in remain_cell_idx:
				common_values = set(cells_status[idx][1]) & set(triple)
				if len(common_values) > 0:
					print("=================== [Naked_Triples] =================== ")
					print("* Change cell", idx)
					print("domain_col", domain_col)
					print("triple", triple)
					print("* Previous", cells_status[idx])
					cells_status[idx][1] = list(set(cells_status[idx][1]) - set(common_values))
					print("* After", cells_status[idx])
					changed = True
	return changed

def hidden_triples(cells_status, slot_idx):
	changed = False
	domain_col = [cells_status[x][1] for x in slot_idx]
	flat_list = [item for sublist in domain_col for item in sublist]
	triple_list = list(itertools.combinations(set(flat_list), 3))

	for triple in triple_list:
		cell_idx = [slot_idx[index] for index, value in enumerate(domain_col)
								if 	len(value) > 0 and
									len(set(triple) & set(value)) > 0]
		if len(cell_idx) == 3:
			for idx in cell_idx:
				common_values = list(set(triple) & set(cells_status[idx][1]))
				remove_values = list(set(cells_status[idx][1]) - set(common_values))
				if len(common_values) > 0 and len(remove_values) > 0:
					print("=================== [Naked_Triples] =================== ")
					print("* Change cell", idx)
					print("domain_col", domain_col)
					print("triple", triple)
					print("* Previous", cells_status[idx])
					cells_status[idx][1] = list(set(triple) & set(cells_status[idx][1]))
					print("* After", cells_status[idx])
					changed = True
			#break
			return changed
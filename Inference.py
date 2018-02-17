from utility import *
import collections

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
	count_idx_list = [index for index, value in enumerate(counter_values) if value == 1]
	#for count_idx in count_idx_list:
	if len(count_idx_list) > 0:
		count_idx = count_idx_list[0]
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


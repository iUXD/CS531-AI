from heapq import heapify, heappop, heappush
from utility import *

def MCV(cells_status):
    # Most Constrained Variable, used a heap
    pq = []  # heap
    heapify(pq)
    for i in range(81):
        if len(cells_status[i][1]) != 1:
            heappush(pq, (len(cells_status[i][1]), i))
    pass
from tqdm import tqdm

import time


abc = ["hey", "du", "dort"]

nodes = tqdm(list([]), "nodes finished: ", ncols=100, total=3)
nodes.update(1)
time.sleep(1)
nodes.iterable.append("das bin ich")
nodes.update(1)
time.sleep(1)
nodes.iterable.append("das bin ich2222")
nodes.se
time.sleep(1)
nodes.iterable.append("und wer bist du")
nodes.update(1)
time.sleep(1)


# for node in nodes:
# print(f"bin bei node: {node}")
# time.sleep(1)



from spn.io.Text import str_to_spn

f = open("D:\\Repos\\PPSPN\\ressources\\input\\bnetflix\\spn.in", "r")
spn_str = f.read()
spn = str_to_spn(spn_str)




from spn.algorithms.Statistics import get_structure_stats
from spn.io.Graphics import plot_spn
from spn.structure.Base import assign_ids, rebuild_scopes_bottom_up

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

print("===============================")
print("bnetflix")
print(get_structure_stats(str_to_spn(open("D:\\Repos\\PPSPN\\ressources\\input\\bnetflix\\spn.in", "r").read())))
print("===============================")

print("===============================")
print("baudio")
print(get_structure_stats(str_to_spn(open("D:\\Repos\\PPSPN\\ressources\\input\\baudio\\spn.in", "r").read())))
print("===============================")

print("===============================")
print("jester")
print(get_structure_stats(str_to_spn(open("D:\\Repos\\PPSPN\\ressources\\input\\jester\\spn.in", "r").read())))
print("===============================")

print("===============================")
print("nltcs")
spn_nltcs = str_to_spn(open("D:\\Repos\\PPSPN\\ressources\\input\\nltcs\\spn.in", "r").read())
assign_ids(spn_nltcs)
rebuild_scopes_bottom_up(spn_nltcs)
plot_spn(spn_nltcs, 'plots/nltcsSPN.png')
print(get_structure_stats(spn_nltcs))
print("===============================")


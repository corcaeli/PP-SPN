# from tabulate import tabulate
import pandas

namen = ["hallo", "ich", "bin", "eine", "tabelle"]
werte_1 = [1, 2, 3, 4, 5]
werte_2 = ["a", "b", "c", "d", "e"]
werte_3 = [6, 7, 8, 9, 10]
werte = [werte_1, werte_2, werte_3]
print(pandas.DataFrame(werte, columns=namen))

print(pandas.DataFrame(namen, werte))

abc = ["ab", 5, "def"]
print(abc)

my = list(map(lambda row: row + ["hey"], werte))
print(my[0][-1])
print(my)

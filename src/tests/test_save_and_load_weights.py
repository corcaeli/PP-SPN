path = "/home/nick/PPSPN/tests/spn_weights_test.in"

f = open(path, "w")

f.write("(0, 1)=10\n")
f.write("(1, 12)=5343\n")
f.write("(3, 4)=1652\n")
f.close()

f2 = open(path, "r")

data = {}
for line in f2.read().splitlines():
    data_id, value_str = line.split("=")
    value = int(value_str)

    data[data_id] = value

f2.close()
print(data)

import math

d = 10000000
digits = round(math.log(d, 10) / 2)
# print(digits)

import numpy as np


def myround(num):
    return int(num)


print(round(0.5))
print(round(1.5))
print(round(2.5))
print(round(3.5))
print(round(4.5))
print(round(5.5))
print(round(6.5))
print(round(7.5))

print("============")

print(myround(0.5))
print(myround(1.5))
print(myround(2.5))
print(myround(3.5))
print(myround(4.5))
print(myround(5.5))
print(myround(6.5))
print(myround(7.5))


abc = [1, 5, 3, 2.2]
print(abc)
print(type(abc))

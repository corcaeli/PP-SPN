import math

muliplyer = pow(10, 17)
precision = math.log10(muliplyer) // 2 - 1
print(muliplyer)
print(precision)

a = 0.00000001
b = 0.00000001
c = a * b
a_multiplyer = a * muliplyer
b_multiplyer = b * muliplyer
print(a_multiplyer)
print(b_multiplyer)
c_mult = (a_multiplyer * b_multiplyer) / muliplyer
print(c_mult)

"load_private_data_from_file".ljust(10, ".")
print(len("load_private_data_for_private_evaluation_from_file"))

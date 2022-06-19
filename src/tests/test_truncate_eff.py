import random

p = 53

s = 6
x_1, x_2, x_3 = 2, 4, 3  # x=9

r = random.randint(0, p // 2)  # public
r = 17
r_1, r_2, r_3 = 5, 3, 9  # shares von r

z = r % s  # = 5
z_1, z_2, z_3 = 2, 1, 2


helper_1 = x_1 + z_1  # =2+5=7
helper_2 = x_2 + z_2  # =4+3=7
helper_3 = x_3 + z_3  # =5+9=12

helper = helper_1 + helper_2 + helper_3  # =7+7+12 = 26


h = helper % s  # 26%6 = 2
h_1, h_2, h_3 = 15, 29, 11


d_1 = x_1 - h_1 + z_1  # = 2 - 15 + 2 = -11 = 42
d_2 = x_2 - h_2 + z_2  # = 4 - 29 + 1 = -24 = 29
d_3 = x_3 - h_3 + z_3  # = 3 - 11 + 2 = -6 = 47

s_inv = pow(s, p - 2, p)


# z = r % s
# helper = x + r
# h = (x+r) % s
# result = (x - ((x+r) % s) + (r%s)) / s
# = (x - (x%s) - (r%s) + (r%s)) / s
# = (x - x%s) / s
# = x //s

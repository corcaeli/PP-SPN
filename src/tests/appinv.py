from decimal import *
import math
from tqdm import tqdm

# glob_t = 13
# glob_k = 13
# glob_n = 48
# glob_l = 20

# glob_prim braucht 74 bits zur darstellung
# glob_prim = 13558774610046711780701

# glob_n = 1024
glob_n = 48
glob_p = 128
glob_k = 10
glob_tau = 4
# secrets are 0 < value < 2^n
# glob_t = 30
glob_t = 13
glob_w = glob_n + 30
glob_l = glob_n

glob_prim = pow(2, 1200) + 1515

print(glob_prim)

upper_appinv_error_bound = Decimal(glob_k + 1) / Decimal(pow(2, glob_t - 4))
upper_trunc_error_bound = glob_k + 1


def trunc(a, n):
    # tmp = Decimal(a) / Decimal(pow(2, n))
    # print(f"trunc: {a} with {n}")
    tmp = a / pow(2, n)
    return math.trunc(tmp)


def trunc_error(a, n):
    b = trunc(a, n)
    return abs(b - Decimal(a) / Decimal(pow(2, n)))


def appinv(p):
    return appinv_alt(p)


def appinv_orig(p):
    print("App inv method start")
    u = 3 * pow(2, glob_t - 1)
    amount_round = math.ceil(math.log(glob_t - 3 - math.log(glob_k + 1, 2), 2))
    for i in range(amount_round):  # not -1 cause range is exclusive the given bound
        z = p * u
        w = trunc(z, glob_n)
        v = pow(2, glob_t + 1) * u - w * u
        u = trunc(v, glob_t)

    return u


def appinv_alt(p):
    u = 3 * pow(2, glob_t - 1)
    amount_round = 100
    for i in tqdm(
        range(amount_round), f"appinv for {p}"
    ):  # not -1 cause range is exclusive the given bound
        z = p * u
        w = pow(2, glob_n + glob_t + 1) * u - z * u
        v = trunc(w, glob_n)
        u = trunc(v, glob_t)
        # print(f"z = {z}\t w = {w}\t v = {v}\t u = {u}")
    print(u)
    return u


def appinv_error(p):
    p_tilde = appinv(p)

    return abs(
        Decimal(pow(2, glob_n)) / Decimal(p)
        - Decimal(p_tilde) / Decimal(pow(2, glob_t))
    )


def mod(c, p, p_tilde=None):
    if p_tilde is None:
        p_tilde = appinv_alt(p)
    c_tilde = trunc(c, glob_l)
    q_hat = c_tilde * p_tilde
    q = trunc(q_hat, glob_n + glob_t - glob_l)
    return c - p * q


print(f"\nUpper trunv error bound: {upper_trunc_error_bound}")
trunc_values = [
    (156542342324, 30),
    (626169369296 * 1000, 46),
    (2132133, 16),
    (55233222, 60),
    (23455, 8),
    (75438, 32),
]
# for a, n in trunc_values:
#    err = trunc_error(a, n)
#    print(
#        f"In Bound?: {err <= upper_trunc_error_bound} for trunc error {err} for input ({a}, {n})"
#    )

print(f"\nUpper appinv error bound: {upper_appinv_error_bound}")
appinv_values = [
    156542342324,
    2132133,
    55233222,
    23455,
    75438,
    626169369296,  # * pow(2, 30),
]
# for value in appinv_values:
#    err = appinv_error(value)
#    print(
#        f"In Bound?: {err <= upper_appinv_error_bound} for appinv error {err} for input ({value})"
#    )


print(f"\nModulo Protocol:")
mod_values = [
    (16, 11),
    (626169369296, 2132133),
    (26, 10),
    (4322254, 34232),
    (100, 10),
    (123, 25),
    (626169369296, 23455),
]
# for c, p in mod_values:
#    mod_result = mod(c, p)
#    python_mod_result = c % p
#    print(f"For input ({c}, {p}) python: {python_mod_result}\t paper: {mod_result}")


prim = 13558774610046711780701  # pow(2, 1200) + 1515
# prim = 7
m = prim // 2 - 1
import random


def rounded_division(x, s):
    r = random.randint(1, m)
    z = r % s
    manager_tmp = r + x
    h = manager_tmp % s
    member_tmp = x - h + z
    # member_tmp = x - ((r+x) % s) + (r%s)
    member_tmp2 = (member_tmp * pow(s, prim - 2, prim)) % prim
    return member_tmp2


div_values = [
    (16, 11),
    (323, 56),
    (26, 6),
    (114, 8),
    (885, 250),
    (942, 811),
    (45, 5),
]
for x, s in div_values:
    lower_bound = math.floor(x / s)
    upper_bound = math.ceil(x / s)
    my_value = rounded_division(x, s)
    print(
        f"{lower_bound} <= {my_value} <= {upper_bound} ? \t{lower_bound <= my_value and my_value <= upper_bound}\treal value: {x/s}"
    )

n = 5


# def appinv(p):
#    i = 1
#    u = 3 * pow(2, n - 2)
#    while i <= n + 5:  # not -1 cause range is exclusive the given bound
#        x = u * p
#        y = rounded_division(x, pow(2, n))  # trunc(x, n) # x / pow(2, n)
#        z = u * (pow(2, n + 1) - y)
#        u = rounded_division(z, pow(2, n))  # trunc(z, n) #z / pow(2, n)
#        # u = u * (pow(2, n + 1) - p * u / pow(2, n)) / pow(2, n)
#        i = i + 1
#        print(f"p: {p}\ti: {i}\tu: {u}")
#    return u


# def test(p):
#    print(pow(2, 2 * n) / p, appinv(p))

n = 18
t = 7


def appinv(p):
    print(f"appinv for {p}")
    i = 1
    u = 3 * pow(2, t - 2)
    while i <= n + t:  # use the iteration bound of the paper + n
        tmp = p * u
        print(f"p = {p} und u = {u}")
        z = trunc(tmp, t)  # p * u // pow(2, t)
        y = pow(2, n + 1) - z
        x = u * y
        u = trunc(x, n)  # x // pow(2, n)
        print(f"\nIteration: {i}")
        print(f"tmp: {tmp}\nz: {z}\ny: {y}\nx: {x}\nu: {u}")
        i = i + 1
    w = u + pow(2, t - 1)
    u = trunc(w, t)  # (u + pow(2, t - 1)) // pow(2, t)
    print(f"w: {w}")
    print(f"final u: {u}")
    return u


def test(p):
    print(pow(2, n) / p, appinv(p))


print("========= line")
# test(1)
# test(pow(2, n - 1))
# test(5)
# test(234)
test(632)
# print("sadsdadsa")
# print(pow(2, n))
# print(appinv(632) * 632)
# print(trunc(appinv(632), n))


print("=====abc====")
# test(1)
print("=====xxx====")
# test(pow(2, n - 1))
print("=====def====")
# test(pow(2, n // 2))
print("=====ghi====")
# test(2)
print("=====ghi====")
# test(5)
print("=====ghi====")


def mod(c, p, p_tilde=None):
    if p_tilde is None:
        p_tilde = appinv(p)
    c_tilde = trunc(c, n)  # glob_l hunten
    q_hat = c_tilde * p_tilde
    q = trunc(q_hat, n + t - 32)  # glob l hinten
    return c - p * q


def divi(c, p, p_tilde=None):
    if p_tilde is None:
        p_tilde = appinv(p)
    tmp = p_tilde * c  # glob_l hunten
    # q_hat = c_tilde * p_tilde
    q = trunc(tmp, n)  # glob l hinten
    print(f"denom_appinv: {p_tilde}\ntmp: {tmp}\nresult: {q}\n")
    return q


print(f"divi: {divi(320, 34)}")
print(f"\nModulo Protocol:")
# mod_values = [
#    (16, 11),
#    (626169369296, 2132133),
#    (26, 10),
#    (4322254, 34232),
#    (100, 10),
#    (123, 25),
#    (626169369296, 23455),
# ]

mod_values = [
    (16, 11),
    (323, 56),
    (26, 6),
    (114, 8),
    (885, 250),
    (942, 811),
    (45, 5),
]
# for c, p in mod_values:
#    div_result = divi(c, p)
#    python_div_result = c / p
#    print(f"For input ({c}, {p}) python: {python_div_result}\t paper: {div_result}")


# print(f"appinv(320) = {appinv(320)}")
# print(f"appinv(3124) = {appinv(3124)}")

# print(f"trunc(31247* pow(2,64)) = {trunc(31247 * pow(2,64),48)}")
# print(f"trunc(31247*100000000000000000) = {trunc(3124*100000000000000000,16)}")
# print(f"appinv(6767) = {appinv(6767)}")  # 634693 by 32 and 10 by 16


# print(f"trunc(162408, 16) = {trunc(162408, 16)}")
d = pow(2, 33)  # pow(2, 32) # 100000000000000000

num_1 = 3123
num_2 = 122
div = 6767

# a = divi(num_1 * d, div)
##b = divi(num_2 * d, div)
# print(f"divi({num_1*d}, {div}) = {a}")  # 46165

# print(f"divi({num_2*d}, {div}) = {b}")  # 46165

# c = a * b
# print(f"c = {c}")
# tmp_result = c / d
# print(f"div by d = {tmp_result}")
# print(f"result = {tmp_result/d}")

# print(f"real = {(num_1/div)*(num_2/div)}")
# print(f"trunc(162408) = {trunc(1627, 5)}")

# n = 24
# t = 8
# p = 256
# print(appinv(473623))
# pow(2,32) / pow(2,16)


# 162408
# 13295900877.
# print(f"trunc(6767, 16) = {trunc(6767, 5)}")  #
# print(f"trunc(31247, 16) = {trunc(31247*pow(2,32), 16)}")

import math


def trunc(a, n):
    # tmp = Decimal(a) / Decimal(pow(2, n))
    # print(f"trunc: {a} with {n}")
    tmp = a / n
    return math.trunc(tmp)


n = 18
t = 7


def appinv0(p):
    print(f"appinv for {p}")
    i = 1
    u = 3 * pow(2, t - 2)
    while i <= t + n:  # use the iteration bound of the paper + n
        tmp = p * u
        print(f"p = {p} und u = {u}")
        z = trunc(tmp, pow(2, t))  # p * u // pow(2, t)
        y = pow(2, n + 1) - z
        x = u * y
        u = trunc(x, pow(2, n))  # x // pow(2, n)
        print(f"\nIteration: {i}")
        print(f"tmp: {tmp}\nz: {z}\ny: {y}\nx: {x}\nu: {u}")
        i = i + 1
    w = u + pow(2, t - 1)
    u = trunc(w, pow(2, t))  # (u + pow(2, t - 1)) // pow(2, t)
    print(f"w: {w}")
    print(f"final u: {u}")
    return u


def appinv(x):
    i = 1
    u = 3 * pow(2, t - 2)
    while i <= n + t:  # use the iteration bound of the paper + n
        tmp = x * u
        z = trunc(tmp, pow(2, t))
        y = 2 * (pow(2, n) + x) - z
        p = u * y
        u = trunc(p, pow(2, n) + x)

        i = i + 1

    w = u + pow(2, t - 1)
    u = trunc(w, pow(2, t))
    return u


d_multi = pow(2, n)  # =8192


def division0(numerator, denominator):
    print(f"appinv for {denominator}")
    i = 1
    u = 3 * pow(2, t - 2)
    u = d_multi * pow(2, t)
    print(f"u: {u}")
    # denominator = denominator * d_multi
    while i <= t + n:  # use the iteration bound of the paper + n
        tmp = denominator * u
        print(f"p = {denominator} und u = {u}")
        z = trunc(tmp, pow(2, t))  # p * u // pow(2, t)
        y = 2 * d_multi * (numerator + denominator) - z
        x = u * y
        u = trunc(x, d_multi * (numerator + denominator))  # x // pow(2, n)

        print(f"\nIteration: {i}")
        print(f"tmp: {tmp}\nz: {z}\ny: {y}\nx: {x}\nu: {u}")
        i = i + 1
    w = u + pow(2, t - 1)
    u = trunc(w, pow(2, t))  # (u + pow(2, t - 1)) // pow(2, t)
    u = trunc(u, d_multi) - 1

    print(f"w: {w}")
    print(f"final u: {u}")
    return u


def division(numerator, denominator):
    print(f"appinv for {denominator}")
    i = 1
    u = 3 * pow(2, t - 2)
    print(f"u: {u}")
    # denominator = denominator * d_multi
    while i <= t + n:  # use the iteration bound of the paper + n
        tmp = denominator * u
        z = trunc(tmp, pow(2, t))
        y = 2 * (numerator + denominator) - z
        x = u * y
        u = trunc(x, (numerator + denominator))

        print(f"\nIteration: {i}")
        print(f"tmp: {tmp}\nz: {z}\ny: {y}\nx: {x}\nu: {u}")
        i = i + 1
    w = u + pow(2, t - 1)
    u = trunc(w, pow(2, t))  # (u + pow(2, t - 1)) // pow(2, t)
    u = trunc(u, d_multi) - 1

    print(f"w: {w}")
    print(f"final u: {u}")
    return u


def test(numerator, denominator):
    print((numerator + denominator) / denominator - 1, division(numerator, denominator))


print("========= line")
# test(1)
# test(pow(2, n - 1))
# test(5)
# test(234)
#########test(223 * d_multi, 123456)
print(trunc(54354587, 2564))
# print("sadsdadsa")
# print(pow(2, n))
# print(appinv(632) * 632)
# print(trunc(appinv(632), n))

# print(trunc(56643, 15))
# print("=====abc====")
# test(1)
# print("=====xxx====")
# test(pow(2, n - 1))
# print("=====def====")
# test(pow(2, n // 2))
# print("=====ghi====")
# test(2)
# print("=====ghi====")
# test(5)
# print("=====ghi====")


def appinv(x):
    i = 1
    u = 3 * pow(2, t - 2)
    while i <= n + t:  # use the iteration bound of the paper + n
        tmp = x * u
        z = trunc(tmp, pow(2, t))
        y = 2 * (pow(2, n) + x) - z
        x = u * y
        u = trunc(x, pow(2, n) + x)
        print(f"\nIteration: {i}")
        print(f"tmp: {tmp}\nz: {z}\ny: {y}\nx: {x}\nu: {u}")
        i = i + 1

    w = u + pow(2, t - 1)
    u = trunc(w, pow(2, t))
    return u


def appinv0(p):
    i = 1
    u = 3 * pow(2, t - 2)
    while i <= t + n:  # use the iteration bound of the paper + n
        tmp = p * u
        z = trunc(tmp, pow(2, t))  # p * u // pow(2, t)
        y = (pow(2, n+1) ) - z  # pow(2, n + 1) + 2 * p - z
        x = u * y
        u = trunc(x, pow(2, n))  # x // pow(2, n)
        print(f"\nIteration: {i}")
        print(f"tmp: {tmp}\nz: {z}\ny: {y}\nx: {x}\nu: {u}")
        i = i + 1
    w = u + pow(2, t - 1)
    u = trunc(w, pow(2, t))  # (u + pow(2, t - 1)) // pow(2, t)
    print(f"w: {w}")
    print(f"final u: {u}")
    return u


n = 18
t = 5

def test(denominator):
    print((pow(2, n) ) / denominator, appinv0(denominator))

print(f"n = {n}")           # 2^n = 262.144
test(54226)

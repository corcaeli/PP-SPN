from math import floor


def paper_calculate(prim_number, d, num, den):
    dn = d * num
    id = pow(int(den), prim_number - 2, prim_number) % prim_number
    rdn = (dn % den) % prim_number  # important dn % den and NOT dn % id
    w = ((dn - rdn) * id) % prim_number
    return w


def expected(prim_number, d, num, den):
    return floor(d * (num) / den)


res = paper_calculate(59, 100, 5, 9)
expected_result = expected(59, 100, 5, 9)
print(f"paper_calculation: {res}\t expected: {expected_result}")

res = paper_calculate(103, 65, 5, 9)
expected_result = expected(103, 65, 5, 9)
print(f"paper_calculation: {res}\t expected: {expected_result}")

res = paper_calculate(283, 65, 5, 9)
expected_result = expected(283, 65, 5, 9)
print(f"paper_calculation: {res}\t expected: {expected_result}")


res = paper_calculate(1229, 100, 5, 9)
expected_result = expected(1229, 100, 5, 9)
print(f"paper_calculation: {res}\t expected: {expected_result}")


res = paper_calculate(31249, 1000, 5, 9)
expected_result = expected(31249, 1000, 5, 9)
print(f"paper_calculation: {res}\t expected: {expected_result}")


res = paper_calculate(50753, 2000, 5, 9)
expected_result = expected(50753, 2000, 5, 9)
print(f"paper_calculation: {res}\t expected: {expected_result}")

res = paper_calculate(31249, 1000, 9, 5)
expected_result = expected(31249, 1000, 9, 5)
print(f"paper_calculation: {res}\t expected: {expected_result}")


res = paper_calculate(50753, 2000, 9, 5)
expected_result = expected(50753, 2000, 9, 5)
print(f"paper_calculation: {res}\t expected: {expected_result}")


# print(type(bin(17)))

# print(pow(int(9), 17 - 2, 17))
# print(gf_invert(9))

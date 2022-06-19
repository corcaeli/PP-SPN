from Cryptodome.Protocol.SecretSharing import Shamir
from Cryptodome.Util.number import long_to_bytes, bytes_to_long

k = 4
n = 5

name_to_private_inputs = {"a": 147, "b": 8645678, "c": 20092, "d": 18498, "e": 5395}

name_to_shares = {}
for name, value in name_to_private_inputs.items():
    name_to_shares[name] = Shamir.split(k, n, value)
    # print(f"{name} with value {value} got shares {name_to_shares[name]}")

print("=================")
e_shares = name_to_shares.get("e")
print(e_shares)
e_shares_as_long = list(
    map(
        lambda share: (share[0], bytes_to_long(share[1])),
        e_shares,
    )
)
print(e_shares_as_long)
print("========xx=========")

name_to_recombined_private_inputs = {}
for name, shares in name_to_shares.items():
    value = bytes_to_long(Shamir.combine(shares))
    name_to_recombined_private_inputs[name] = value
    print(f"For {name} we got the value {value}")


# sum testing

first_summand_name = "a"
second_summand_name = "e"

first_summand_shares = name_to_shares.get(first_summand_name)
second_summand_shares = name_to_shares.get(second_summand_name)

import numpy as np

# sum_result at index 0 is never used
sum_result_bytes = np.full(n + 1, None)
for (index, first_summand_share) in first_summand_shares:
    sum_result_bytes[index] = first_summand_share

for (index, second_summand_share) in second_summand_shares:
    sum_result_bytes[index] += second_summand_share

sum_result_longs = np.full(n + 1, None)
for (index, first_summand_share) in first_summand_shares:
    sum_result_longs[index] = bytes_to_long(first_summand_share)

for (index, second_summand_share) in second_summand_shares:
    sum_result_longs[index] += bytes_to_long(second_summand_share)


for index in range(n + 1):
    print(f"index = {index}")
    sum_result_long = sum_result_longs[index]
    sum_result_byte = sum_result_bytes[index]
    if (sum_result_long is not None) and (sum_result_byte is not None):
        print(f"\tsr_long = {sum_result_long}")
        print(f"\tsr_byte = {sum_result_byte}")
        print(f"\tsr_byte_as_long = {bytes_to_long(sum_result_byte)}")


# irr_poly = 1 + 2 + 4 + 128 + 2 ** 128
# print(f"irr_poly = {irr_poly}")
sum_result = sum_result_longs
sum_result_shares = []
for index in range(n + 1):
    if sum_result[index] is not None:
        sum_result_shares.append((index, sum_result[index]))

print(f"result_shares = {sum_result_shares}")
sum_result_decoded = bytes_to_long(Shamir.combine(sum_result_shares))
print(f"result_decoded = {sum_result_decoded}")

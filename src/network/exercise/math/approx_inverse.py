from globals import DataIDs, Values
import math
from network.exercise.reveal.reveal_number import add_exercise_reveal_number

from network.exercise.util.manager_inser_in_share import (
    add_exercise_manager_inser_in_share,
)
from network.exercise.math.multiplication import add_exercise_multiplication
from network.exercise.math.trunc import add_exercise_trunc
from network.exercise.math.multiplication_with_clear_value import (
    add_exercise_multiplication_with_clear_value,
)
from network.exercise.math.subtraction import add_exercise_subtraction
from network.exercise.math.addition import add_exercise_addition

from network.exercise.joint_random_sharing_of_zero.jrpz import add_exercise_jrpz

from network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids
from network.exercise.util.copy_data import add_exercise_copy_data


def add_exercise_approx_inverse(manager, data_id, data_id_result=None):
    # appinv(x) = 2^n / x

    n = manager.truncate_n
    t = manager.truncate_t
    k = manager.amount_members

    data_id_u = f"{data_id}_approx_inverse_u"
    data_id_tmp = f"{data_id}_approx_inverse_tmp"
    data_id_z = f"{data_id}_approx_inverse_z"
    data_id_y = f"{data_id}_approx_inverse_y"
    data_id_x = f"{data_id}_approx_inverse_x"
    data_id_w = f"{data_id}_approx_inverse_w"

    manager.data[data_id_u] = 3 * pow(2, t - 2)
    # print(3 * pow(2, t - 2))
    add_exercise_manager_inser_in_share(manager, data_id_u)
    ##add_exercise_copy_data(manager, DataIDs.DIVISION_MULTIPLYER, data_id_u)

    # if manager.data.get(data_id_pow_2_to_n_plus_1) is None:
    #    manager.data[data_id_pow_2_to_n_plus_1] = pow(2, n + 1)
    #    manager.data[data_id_pow_2_to_t_minus_1] = pow(2, t - 1)
    #    add_exercise_manager_inser_in_share(manager, data_id_pow_2_to_n_plus_1)
    #    add_exercise_manager_inser_in_share(manager, data_id_pow_2_to_t_minus_1)
    # amount_rounds = math.ceil(math.log(t - 3 - math.log(k + 1, 2), 2))
    amount_rounds = t
    # print(f"amount rounds+n = {amount_rounds + n}")
    i = 1
    while i <= amount_rounds + n:
        add_exercise_multiplication(
            manager, data_id, data_id_u, data_id_tmp
        )  # tmp = p * u
        add_exercise_trunc(manager, data_id_tmp, t, data_id_z)  # z = trunc(tmp, t)
        add_exercise_subtraction(
            manager, DataIDs.APPINVERSE_OF_TWO_POW_N_PLUS_1, data_id_z, data_id_y
        )  # y = pow(2, n + 1) - z
        add_exercise_multiplication(
            manager, data_id_u, data_id_y, data_id_x
        )  # x = u * y
        add_exercise_trunc(manager, data_id_x, n, data_id_u)  # u = trunc(x, n)
        i = i + 1
        add_exercise_reveal_number(manager, data_id_tmp)
        add_exercise_reveal_number(manager, data_id_z)
        add_exercise_reveal_number(manager, data_id_y)
        add_exercise_reveal_number(manager, data_id_x)

    add_exercise_addition(
        manager, data_id_u, DataIDs.APPINVERSE_OF_TWO_POW_T_MINUS_1, data_id_w
    )  # w = u + pow(2, t - 1)
    add_exercise_trunc(manager, data_id_w, t, data_id_result)  # u = trunc(w, t)

    add_exercise_reveal_number(manager, data_id_w)

    add_exercise_delete_data_at_ids(
        manager, data_id_u, data_id_tmp, data_id_z, data_id_y, data_id_x, data_id_w
    )


def add_exercise_approx_inverse_old(manager, data_id, data_id_result=None):

    k = manager.amount_members
    log_k = math.ceil(math.log(k, 2))
    n = manager.additive_sharing_over_integer_allowed_bit_length_of_secret
    t = (
        math.floor(math.log(manager.prim_number, 2))
        - manager.additive_sharing_over_integer_security_parameter
        - log_k
        - 6
        - n
    )
    # print(f"k = {k}\nlog_k = {log_k}\nn = {n}\nt = {t}")

    data_id_u = f"{data_id}_approx_inverse_u"
    data_id_z = f"{data_id}_approx_inverse_z"
    data_id_w = f"{data_id}_approx_inverse_w"
    data_id_v = f"{data_id}_approx_inverse_v"

    data_id_to_subtract = f"{data_id}_approx_inverse_to_subtract"
    data_id_subtract_target = f"{data_id}_approx_inverse_subtract_target"
    data_id_0 = f"{data_id}_approx_inverse_0"

    manager.data[data_id_u] = 3 * pow(2, t - 1)
    add_exercise_manager_inser_in_share(manager, data_id_u)
    amount_rounds = math.ceil(math.log(t - 3 - math.log(k + 1, 2), 2))

    for round in range(amount_rounds):
        add_exercise_multiplication(manager, data_id, data_id_u, data_id_z)
        add_exercise_trunc(manager, data_id_z, n, data_id_w)
        add_exercise_multiplication(manager, data_id_w, data_id_u, data_id_to_subtract)
        add_exercise_multiplication_with_clear_value(
            manager, data_id_u, pow(2, t + 1), data_id_subtract_target
        )
        add_exercise_subtraction(
            manager, data_id_subtract_target, data_id_to_subtract, data_id_v
        )

        add_exercise_trunc(manager, data_id_v, t, data_id_u)
    add_exercise_jrpz(manager, data_id_0)
    add_exercise_addition(manager, data_id_u, data_id_0, data_id_result)
    add_exercise_delete_data_at_ids(
        manager,
        data_id_u,
        data_id_z,
        data_id_w,
        data_id_v,
        data_id_0,
        data_id_to_subtract,
        data_id_subtract_target,
    )

from globals import DataIDs, Values
from network.exercise.joint_random_sharing_of_zero.jrpz import add_exercise_jrpz

from network.exercise.math.multiplication_with_clear_value import (
    add_exercise_multiplication_with_clear_value,
)
from network.exercise.math.multiplicative_inverse import (
    add_exercise_multiplicative_inverse,
)
from network.exercise.math.modulo import add_exercise_modulo
from network.exercise.math.subtraction import add_exercise_subtraction
from network.exercise.math.multiplication import add_exercise_multiplication
from network.exercise.math.approx_inverse import add_exercise_approx_inverse
from network.exercise.math.trunc import add_exercise_trunc
from network.exercise.reveal.reveal_number import add_exercise_reveal_number

from network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids
from network.exercise.math.addition import add_exercise_addition


def add_exercise_division(
    manager, data_id_numerator, data_id_denominator, data_id_result
):
    data_id_calculation = f"{data_id_numerator}_div_{data_id_denominator}"
    data_id_dn = f"{data_id_calculation}_dn"
    data_id_denominator_appinv = f"{data_id_calculation}_denominator_appinv"
    data_id_tmp = f"{data_id_calculation}_tmp"

    ##new
    ##data_id_pre_add = f"{data_id_calculation}_pre_add"
    # pre_add = num+den
    ##add_exercise_addition(
    ##    manager, data_id_numerator, data_id_denominator, data_id_pre_add
    ##)

    ##new
    # dn = (num+den) * d
    ##add_exercise_multiplication_with_clear_value(
    ##    manager, data_id_pre_add, manager.d_multiplyer, data_id_dn
    ##)
    add_exercise_multiplication_with_clear_value(
        manager, data_id_numerator, manager.d_multiplyer, data_id_dn
    )

    add_exercise_approx_inverse(
        manager, data_id_denominator, data_id_denominator_appinv
    )

    add_exercise_multiplication(
        manager, data_id_dn, data_id_denominator_appinv, data_id_tmp
    )

    ##new
    add_exercise_subtraction(
        manager, data_id_tmp, DataIDs.DIVISION_MULTIPLYER, data_id_tmp
    )
    add_exercise_trunc(manager, data_id_tmp, manager.truncate_n, data_id_result)

    add_exercise_reveal_number(manager, data_id_dn)
    add_exercise_reveal_number(manager, data_id_denominator_appinv)
    add_exercise_reveal_number(manager, data_id_tmp)

    add_exercise_delete_data_at_ids(
        manager, data_id_dn, data_id_denominator_appinv, data_id_tmp
    )


def add_exercise_division_with_d_multiplyer(manager, data_id_numerator, data_id_result):
    data_id_calculation = f"{data_id_numerator}_div_d_multiplyer"
    data_id_denominator_appinv = (
        DataIDs.DIVISION_MULTIPLYER_APPINVERSE
    )  # "d_multiplyer_appinv"
    data_id_tmp = f"{data_id_calculation}_tmp"

    add_exercise_multiplication(
        manager, data_id_numerator, data_id_denominator_appinv, data_id_tmp
    )
    add_exercise_trunc(manager, data_id_tmp, manager.truncate_n, data_id_result)
    # add_exercise_reveal_number(manager, data_id_tmp)

    add_exercise_delete_data_at_ids(manager, data_id_tmp)


def add_exercise_division_old(
    manager, data_id_numerator, data_id_denominator, data_id_result
):
    data_id_calculation = f"{data_id_numerator}_div_{data_id_denominator}"
    data_id_dn = f"{data_id_calculation}_dn"
    data_id_id = f"{data_id_calculation}_id"
    data_id_rdn = f"{data_id_calculation}_rdn"
    data_id_tmp = f"{data_id_calculation}_tmp"

    # dn = d * num
    add_exercise_multiplication_with_clear_value(
        manager, data_id_numerator, manager.d_multiplyer, data_id_dn
    )

    # id = (pow(int(den), prim_number - 2, prim_number) % prim_number)
    add_exercise_multiplicative_inverse(manager, data_id_denominator, data_id_id)

    # rdn = (dn % den) % prim_number  # important dn % den and NOT dn % id
    add_exercise_modulo(manager, data_id_dn, data_id_denominator, data_id_rdn)

    # tmp = dn - rdn
    add_exercise_subtraction(manager, data_id_dn, data_id_rdn, data_id_tmp)

    # w = (tmp * id) % prim_number
    add_exercise_multiplication(manager, data_id_tmp, data_id_id, data_id_result)
    add_exercise_delete_data_at_ids(
        manager, data_id_dn, data_id_id, data_id_rdn, data_id_tmp
    )

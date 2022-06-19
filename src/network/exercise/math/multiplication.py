from network.exercise.exercise_class import Exercise
from globals import IDs

from decimal import Decimal
from decimal import getcontext


def add_exercise_multiplication(
    manager, data_id_a, data_id_b, data_id_result=None, divide_with_d=False
):
    if data_id_result is None:
        data_id_result = data_id_a
    manager.exercises.append(
        Exercise(
            IDs.MULTIPLICATION_INTERMEDIATE_STEP,
            f"{data_id_a};{data_id_b};{data_id_result}",
        )
    )
    manager.exercises.append(
        Exercise(IDs.MULTIPLICATION_RESULT_STEP, f"{data_id_result};{divide_with_d}")
    )


def multiplication_intermediate_step(member, message_value):
    components = message_value.split(";")
    data_id_a = components[0]
    data_id_b = components[1]
    data_id_result = components[2]
    value_a = member.data.get(data_id_a)
    value_b = member.data.get(data_id_b)
    #product = (value_a * value_b) % member.prim_number
    getcontext().prec = 200
    product = int((Decimal(value_a) * Decimal(value_b)) % Decimal(member.prim_number) % member.prim_number)
    member.insert_in_share(f"{data_id_result}_intermediate", int(product))
    member.network_socket.send(
        member.manager_id_chip, IDs.MULTIPLICATION_INTERMEDIATE_STEP, member.id
    )


def multiplication_result_step(member, message_value):
    components = message_value.split(";")
    data_id_result = components[0]
    divide_with_d = components[1] in ["True", "true"]
    member.join_polynomial_shares(f"{data_id_result}_intermediate", data_id_result)
    if divide_with_d:
        #member.data[data_id_result] = (
        #    member.data.get(data_id_result)
        #    * member.d_multiplyer_inverse  # // Values.DIVISION_D_MULTIPLYER
        #) % member.prim_number
        getcontext().prec = 200
        member.data[data_id_result] = int((
            Decimal(member.data.get(data_id_result))
            * Decimal(member.d_multiplyer_inverse)
        ) % Decimal(member.prim_number)) % member.prim_number
    member.network_socket.send(
        member.manager_id_chip, IDs.MULTIPLICATION_RESULT_STEP, member.id
    )

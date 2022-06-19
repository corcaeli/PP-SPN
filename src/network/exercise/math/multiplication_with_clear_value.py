from network.exercise.exercise_class import Exercise
from globals import IDs

from decimal import Decimal
from decimal import getcontext

def add_exercise_multiplication_with_clear_value(
    manager, data_id, value, data_id_result=None
):
    if data_id_result is None:
        data_id_result = data_id
    manager.exercises.append(
        Exercise(
            IDs.MULTIPLICATION_WITH_CLEAR_VALUE,
            f"{data_id};{value};{data_id_result}",
        )
    )


def multiplication_with_clear_value(member, message_value):
    components = message_value.split(";")
    data_id = components[0]
    value = int(components[1])
    data_id_result = components[2]
    #member.data[data_id_result] = (
    #    member.data.get(data_id) * value
    #) % member.prim_number
    getcontext().prec = 100
    member.data[data_id_result] = int((
              Decimal(member.data.get(data_id)) * Decimal(value)
            ) % Decimal(member.prim_number)) % member.prim_number
    member.network_socket.send(
        member.manager_id_chip, IDs.MULTIPLICATION_WITH_CLEAR_VALUE, member.id
    )

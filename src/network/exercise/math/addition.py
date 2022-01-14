from network.exercise.exercise_class import Exercise
from globals import IDs


def add_exercise_addition(manager, data_id_a, data_id_b, data_id_result = None):
    if data_id_result is None:
        data_id_result = data_id_a
    manager.exercises.append(
        Exercise(IDs.ADDITION, f"{data_id_a};{data_id_b};{data_id_result}")
    )


def addition(member, message_value):
    components = message_value.split(";")
    data_id_a = components[0]
    data_id_b = components[1]
    data_id_result = components[2]

    member.data[data_id_result] = (
        member.data.get(data_id_a) + member.data.get(data_id_b)
    ) % member.prim_number
    member.network_socket.send(member.manager_id_chip, IDs.ADDITION, member.id)

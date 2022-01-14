from spn.structure.Base import Sum, get_nodes_by_type
from network.exercise.exercise_class import Exercise
from globals import IDs, Keys


def add_exercise_save_spn_weights_to_file(manager):
    manager.exercises.append(Exercise(IDs.SAVE_SPN_WEIGHTS_TO_FILE))


def save_spn_weights_to_file(member, message_value):
    spn_weights_file_path = member.config[f"ID_{member.id}"].get(
        Keys.CONFIG_SPN_WEIGHTS_FILE_PATH
    )
    f = open(spn_weights_file_path, "w")
    for sum_node in get_nodes_by_type(member.spn, Sum):
        for child_node in sum_node.children:
            data_id_weight = f"({sum_node.id}, {child_node.id})"
            value = member.data.get(data_id_weight)
            f.write(f"{data_id_weight}={value}\n")

    f.close()
    member.network_socket.send(
        member.manager_id_chip, IDs.SAVE_SPN_WEIGHTS_TO_FILE, member.id
    )

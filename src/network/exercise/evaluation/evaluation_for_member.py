import math
from spn.algorithms.Inference import likelihood
from spn.structure.Base import Leaf, get_nodes_by_type
from network.exercise.exercise_class import Exercise
from globals import IDs, Keys, Values

from network.exercise.util.dummy import add_exercise_dummy
from network.exercise.evaluation.evaluate_spn_bottom_up import (
    add_exercise_evaluate_spn_bottom_up,
)

import numpy as np


def add_exercise_evaluation_for_member(
    manager, member_id, line_index_of_input_for_private_evaluation
):
    manager.exercises.append(
        Exercise(
            IDs.EVALUATION_SINGLE_MEMBER_LEAF_STEP,
            f"{member_id};{line_index_of_input_for_private_evaluation}",
        )
    )

    add_exercise_evaluate_spn_bottom_up(manager)
    manager.exercises.append(
        Exercise(IDs.EVALUATION_SEND_TO_SINGLE_MEMBER_STEP, member_id)
    )
    manager.exercises.append(
        Exercise(
            IDs.EVALUATION_SINGLE_MEMBER_JOIN_STEP,
            f"{member_id};{line_index_of_input_for_private_evaluation}",
        )
    )


def evaluation_single_member_leaf_step(member, message_value):
    components = message_value.split(";")
    single_member_id = components[0]
    line_index_of_input_for_private_evaluation = int(components[1])

    if single_member_id == member.id:

        private_data_for_evaluation_file_path = member.config[f"ID_{member.id}"].get(
            Keys.CONFIG_PRIVATE_DATA_FOR_EVALUATION_FILE_PATH
        )

        leaf_nodes = get_nodes_by_type(member.spn, Leaf)
        private_inputs_for_leafes = member.private_data_for_evaluation

        private_input_for_leafes_current_line = private_inputs_for_leafes[
            line_index_of_input_for_private_evaluation
        ]

        private_input_for_leafes = np.array([private_input_for_leafes_current_line])

        for index in range(len(leaf_nodes)):
            leaf_node = leaf_nodes[index]
            # private_input_for_leaf = np.array([[private_input_for_leafes[index]]])

            data_id_leaf_node = f"({leaf_node.id}, {leaf_node.id})_result"
            exact_result = likelihood(leaf_node, private_input_for_leafes)
            digits = int(math.log(member.d_multiplyer, 2) / 2)
            exact_result_rounded = round(exact_result[0][0], digits - 1)
            result_value_for_leaf = math.floor(
                exact_result_rounded * member.d_multiplyer
            )
            member.insert_in_share(
                data_id_leaf_node, result_value_for_leaf, with_id_appendix=False
            )

    member.network_socket.send(
        member.manager_id_chip,
        IDs.EVALUATION_SINGLE_MEMBER_LEAF_STEP,
        member.id,
    )


def evaluation_send_to_single_member_step(member, message_value):
    single_member_id = message_value
    single_member_id_chip = member.id_chips_for_id.get(single_member_id)
    data_id_result = "(0, 0)_result"
    value = member.data.get(data_id_result)
    member.network_socket.send(
        single_member_id_chip, f"{data_id_result}_{member.id}", value
    )
    member.network_socket.send(
        member.manager_id_chip,
        IDs.EVALUATION_SEND_TO_SINGLE_MEMBER_STEP,
        member.id,
    )


def evaluation_single_member_join_step(member, message_value):
    components = message_value.split(";")
    single_member_id = components[0]
    line_index_of_input_for_private_evaluation = int(components[1])

    if single_member_id == member.id:
        data_id_result = "(0, 0)_result"
        member.join_polynomial_shares(data_id_result)
        data_id_to_save = f"eval_{line_index_of_input_for_private_evaluation}_result"
        member.data[data_id_to_save] = member.data.get(data_id_result)
        print(
            f"For member {single_member_id} the {data_id_to_save} is {member.data.get(data_id_to_save)}"
        )
        with open(f"/ppspn_env/ressources/output/evaluation_{single_member_id}.out", "a") as out_file:
            out_file.write(f"{member.data.get(data_id_to_save)}\n")

    member.network_socket.send(
        member.manager_id_chip,
        IDs.EVALUATION_SINGLE_MEMBER_JOIN_STEP,
        member.id,
    )

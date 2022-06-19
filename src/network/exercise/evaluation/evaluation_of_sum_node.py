from network.exercise.math.division import add_exercise_division_with_d_multiplyer
from network.exercise.reveal.reveal_number import add_exercise_reveal_number
from spn.structure.Base import Sum

from network.exercise.math.multiplication import add_exercise_multiplication
from network.exercise.math.addition import add_exercise_addition

from network.exercise.util.copy_data import add_exercise_copy_data
from network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids


def add_exercise_evaluation_of_sum_node(manager, sum_node: Sum):
    data_id_result = f"({sum_node.id}, {sum_node.id})_result"

    manager.data[data_id_result] = 0
    data_ids_to_delete = []
    for index in range(len(sum_node.children)):
        child_node = sum_node.children[index]
        data_id_weight = f"({sum_node.id}, {child_node.id})"
        data_id_child_result = f"({child_node.id}, {child_node.id})_result"

        data_id_child_times_weight = f"({sum_node.id}, {child_node.id})_times_({child_node.id}, {child_node.id})_result"

        add_exercise_multiplication(
            manager,
            data_id_child_result,
            data_id_weight,
            data_id_child_times_weight,
            divide_with_d=False,
        )
        #add_exercise_reveal_number(manager, data_id_child_result)
        #add_exercise_reveal_number(manager, data_id_weight)
        #add_exercise_reveal_number(manager, data_id_child_times_weight)
        add_exercise_division_with_d_multiplyer(
            manager, data_id_child_times_weight, data_id_child_times_weight
        )

        if index == 0:
            add_exercise_copy_data(manager, data_id_child_times_weight, data_id_result)
        else:
            add_exercise_addition(
                manager, data_id_result, data_id_child_times_weight, data_id_result
            )
        data_ids_to_delete.append(data_id_child_times_weight)

    add_exercise_delete_data_at_ids(manager, data_ids_to_delete)

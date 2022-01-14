from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import Sum

from network.exercise.math.division import add_exercise_division

from network.exercise.util.delete_data_at_ids import add_exercise_delete_data_at_ids


def add_exercise_compute_weights(manager):

    data_ids_of_denominators = []
    for sum_node in get_nodes_by_type(manager.spn, ntype=Sum):
        sum_node_id = sum_node.id
        data_id_denominator = f"({sum_node_id}, {sum_node_id})"
        data_ids_of_denominators.append(data_id_denominator)
        for child in sum_node.children:
            child_node_id = child.id
            data_id_numerator = f"({sum_node_id}, {child_node_id})"
            add_exercise_division(
                manager, data_id_numerator, data_id_denominator, data_id_numerator
            )
    ids_to_delete = ";".join(data_ids_of_denominators)
    add_exercise_delete_data_at_ids(manager, ids_to_delete)

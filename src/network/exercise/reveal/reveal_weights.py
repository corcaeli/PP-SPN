from spn.structure.Base import Sum, get_nodes_by_type

from network.exercise.reveal.reveal_number import add_exercise_reveal_number


def add_exercise_reveal_weights(manager):

    for sum_node in get_nodes_by_type(manager.spn, ntype=Sum):
        sum_node_id = sum_node.id
        for child in sum_node.children:
            child_node_id = child.id
            data_id_numerator = f"({sum_node_id}, {child_node_id})"
            add_exercise_reveal_number(manager, data_id_numerator)

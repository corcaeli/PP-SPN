from spn.structure.Base import Leaf, Product, Sum, get_topological_order

from network.exercise.evaluation.evaluation_of_sum_node import (
    add_exercise_evaluation_of_sum_node,
)
from network.exercise.evaluation.evaluation_of_product_node import (
    add_exercise_evaluation_of_product_node,
)


def add_exercise_evaluate_spn_bottom_up(manager):
    """
    Evaluates the spn bottom up
    """

    for node in get_topological_order(manager.spn):
        if isinstance(node, Leaf):
            # self.add_exercise_evaluation_of_leaf_node(node)
            continue
        elif isinstance(node, Sum):
            add_exercise_evaluation_of_sum_node(manager, node)
        elif isinstance(node, Product):
            add_exercise_evaluation_of_product_node(manager, node)
        else:
            raise AssertionError(
                f"Evaluation of node type {node.__class__.__name__} not supported"
            )

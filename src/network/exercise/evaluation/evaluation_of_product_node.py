from spn.structure.Base import Product


from network.exercise.util.copy_data import add_exercise_copy_data
from network.exercise.math.multiplication import add_exercise_multiplication
from network.exercise.math.division import (
    add_exercise_division,
    add_exercise_division_with_d_multiplyer,
)
from network.exercise.math.multiplication_with_clear_value import (
    add_exercise_multiplication_with_clear_value,
)
from network.exercise.reveal.reveal_number import add_exercise_reveal_number
from network.exercise.util.dummy import add_exercise_dummy


def add_exercise_evaluation_of_product_node(manager, product_node: Product):
    data_id_result = f"({product_node.id}, {product_node.id})_result"
    # add_exercise_dummy(manager)
    for index in range(len(product_node.children)):
        child_node = product_node.children[index]
        data_id_child_result = f"({child_node.id}, {child_node.id})_result"
        if index == 0:
            add_exercise_copy_data(manager, data_id_child_result, data_id_result)
        else:
            add_exercise_multiplication(
                manager,
                data_id_result,
                data_id_child_result,
                data_id_result,
                divide_with_d=False,
            )
            add_exercise_division_with_d_multiplyer(
                manager, data_id_result, data_id_result
            )

        ##add_exercise_reveal_number(manager, data_id_child_result)
    ##add_exercise_reveal_number(manager, data_id_result)

    # self.add_exercise_multiplication_with_clear_value

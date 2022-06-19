



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


################################
################################

#add_exercise_evaluation_for_member(
    
#def evaluation_single_member_leaf_step(member, message_value):
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

####

#add_exercise_evaluate_spn_bottom_up(manager):
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
#####
#evaluation_send_to_single_member_step(member, message_value):
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

####
#evaluation_single_member_join_step(member, message_value):
components = message_value.split(";")
single_member_id = components[0]
line_index_of_input_for_private_evaluation = int(components[1])

if single_member_id == member.id:
    data_id_result = "(0, 0)_result"
    member.join_polynomial_shares(data_id_result)
    data_id_to_save = f"eval_{line_index_of_input_for_private_evaluation}_result"
    member.data[data_id_to_save] = member.data.get(data_id_result)










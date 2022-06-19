
for sum_node in spn:
    for product_node in sum_node.children:
        member.used_edges[(sum_node.id, product_node.id)] = 0

#insert edge usage for private_data 
likelihood(spn, member.private_data)

for data_id, value in member.used_edges.items():
    member.insert_in_share(data_id, value)

# adding the usages of one sumnode to child node together
for sum_node in spn:
    for product_node in sum_node.children:
        data_id_numerator = f"({sum_node.id}, {product_node.id})"
        member.data[data_id_numerator] = 0
        for member_id in Network.members:
            member.addTo(data_id_numerator, f"{data_id_numerator}_{member_id}")

# adding the usages of all childs of a sum node together (as denominator)
for sum_node in spn:
    data_id_denominator = f"({sum_node.id}, {sum_node.id})"
    member.data[data_id_denominator] = 0
    for product_node in sum_node.children:
        member.addTo(data_id_denominator, f"({sum_node_id}, {product_node.id})")

for sum_node in spn:
    data_id_denominator = f"({sum_node_id}, {sum_node_id})"
    for product_node in sum_node.children:
        data_id_numerator = f"({sum_node.id}, {product_node.id})"
        add_exercise_division(
            manager, data_id_numerator, data_id_denominator, data_id_numerator
        )
from spn.algorithms.Inference import likelihood
from spn.structure.leaves.parametric.Parametric import Categorical

from spn.structure.Base import Sum, Product, eval_spn_bottom_up, get_nodes_by_type
from spn.structure.Base import assign_ids, rebuild_scopes_bottom_up


def example_spn_from_paper_about_spn():
    # scope 0 = a
    a = Categorical(p=[0.0, 1.0], scope=0)
    a_not = Categorical(p=[1.0, 0.0], scope=0)

    # scope 1 = b
    b = Categorical(p=[0.0, 1.0], scope=1)
    b_not = Categorical(p=[1.0, 0.0], scope=1)

    # scope 2 = c
    c = Categorical(p=[0.0, 1.0], scope=2)
    c_not = Categorical(p=[1.0, 0.0], scope=2)

    n_14 = Sum(weights=[0.1, 0.9], children=[c, c_not])  # 0.1, 0.9
    n_15 = Sum(weights=[0.8, 0.2], children=[c, c_not])
    n_16 = Sum(weights=[0.3, 0.7], children=[c, c_not])

    n_8 = Product(children=[n_14, b])
    n_9 = Product(children=[n_15, b_not])
    n_10 = Product(children=[b, n_16])
    n_11 = Product(children=[b_not, n_16])

    n_6 = Sum(weights=[0.4, 0.6], children=[n_8, n_9])
    n_7 = Sum(weights=[0.5, 0.5], children=[n_10, n_11])

    n_2 = Product(children=[a, n_6])
    n_3 = Product(children=[n_7, a_not])

    n_1 = Sum(weights=[0.3, 0.7], children=[n_2, n_3])

    spn = n_1

    assign_ids(spn)
    rebuild_scopes_bottom_up(spn)

    from spn.io.Text import spn_to_str_equation
    from spn.io.Text import str_to_spn

    spn_str = spn_to_str_equation(spn)
    spn = str_to_spn(spn_str)

    return spn


import numpy as np

spn = example_spn_from_paper_about_spn()
input = np.array([[0, 1, 0]])
result = likelihood(spn, input)
print(result)  # 0.245

input = np.array([[1, 1, 0]])
result = likelihood(spn, input)
print(result)  # 0.108
# likelihood(spn, [input])
from spn.io.Graphics import plot_spn

plot_spn(spn, "spn_rebuild.png")


# f = open("./tests/test_weights_of_paper_spn.out", "w")
# data = {}
# for sum_node in get_nodes_by_type(spn, Sum):
#    children = sum_node.children
#    for index in range(len(children)):
#        child_node = children[index]
#        data_id_weight = f"({sum_node.id}, {child_node.id})"
#        # value = data.get(data_id_weight)
#        value = sum_node.weights[index]
#        f.write(f"{data_id_weight}={value}\n")

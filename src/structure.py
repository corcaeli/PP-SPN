import numpy as np
from spn.structure.Base import Node

from example_spn import example_spn_from_paper_about_spn

# TODO: to implement
def build_spn_structure(data) -> Node:
    assert data is not None
    return example_spn_from_paper_about_spn()


from spn.structure.Base import get_nodes_by_type
from spn.structure.Base import Sum


def change_stuf(node):
    node.weights[0] = 1


def replace_sum_node_weights(spn_root_node, replacement_value=1) -> None:
    sum_nodes = get_nodes_by_type(spn_root_node, Sum)
    for sum_node in sum_nodes:
        sum_node.weights = np.full((len(sum_node.weights)), replacement_value)
        # for index in len(sum_node.weights):
        #    sum_node.weights[index] = 1
    return spn_root_node


def stuf():
    np.random.seed(123)
    train_data = np.c_[
        np.r_[np.random.normal(5, 1, (500, 2)), np.random.normal(10, 1, (500, 2))],
        np.r_[np.zeros((500, 1)), np.ones((500, 1))],
    ]

    from spn.algorithms.LearningWrappers import learn_parametric, learn_classifier
    from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian
    from spn.structure.Base import Context

    spn_classification = learn_classifier(
        train_data,
        Context(parametric_types=[Gaussian, Gaussian, Categorical]).add_domains(
            train_data
        ),
        learn_parametric,
        2,
    )
    # print(train_data)
    test_classification = np.array([3.0, 4.0, np.nan, 12.0, 18.0, np.nan]).reshape(
        -1, 3
    )

    from spn.algorithms.MPE import mpe

    print(mpe(spn_classification, test_classification))

    a = np.random.randint(2, size=1000).reshape(-1, 1)
    b = np.random.randint(3, size=1000).reshape(-1, 1)
    c = np.r_[np.random.normal(10, 5, (300, 1)), np.random.normal(20, 10, (700, 1))]
    d = 5 * a + 3 * b + c
    train_data = np.c_[a, b, c, d]
    # print(d)
    print("=========================")
    print(train_data)

    # MSPN
    from spn.structure.Base import Context
    from spn.structure.StatisticalTypes import MetaType

    # ds_context = Context(meta_types=[MetaType.DISCRETE, MetaType.DISCRETE, MetaType.REAL, MetaType.REAL])
    # ds_context.add_domains(train_data)

    from spn.algorithms.LearningWrappers import learn_mspn

    # mspn = learn_mspn(train_data, ds_context, min_instances_slice=20)

    from spn.io.Graphics import plot_spn

    # plot_spn(mspn, 'plots/mspn.png')

    # parametric SPN
    from spn.structure.Base import Context
    from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian

    ds_context = Context(
        parametric_types=[Categorical, Categorical, Gaussian, Gaussian]
    ).add_domains(train_data)
    spn_classification = learn_classifier(
        train_data,
        Context(
            parametric_types=[Categorical, Categorical, Gaussian, Gaussian]
        ).add_domains(train_data),
        learn_parametric,
        2,
    )

    from spn.algorithms.LearningWrappers import learn_parametric

    # spn = learn_parametric(train_data, ds_context, min_instances_slice=20)
    # plot_spn(spn, 'plots/spn.png')

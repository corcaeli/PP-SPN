from spn.structure.Base import get_nodes_by_type
from spn.structure.leaves.parametric.Parametric import Categorical
from spn.structure.leaves.parametric.Parametric import Leaf
from spn.structure.leaves.parametric.Parametric import Gaussian
from spn.structure.leaves.parametric.Parametric import Uniform
from spn.structure.Base import eval_spn_bottom_up


# add_parametric_inference_support()

from spn.algorithms.Inference import add_node_likelihood, leaf_marginalized_likelihood
from spn.structure.leaves.parametric.Parametric import *
from spn.structure.leaves.parametric.utils import get_scipy_obj_params

from spn.structure.leaves.parametric.Inference import add_parametric_inference_support
from spn.structure.Base import assign_ids, rebuild_scopes_bottom_up


def continuous_likelihood(node, data=None, dtype=np.float64, **kwargs):
    probs, marg_ids, observations = leaf_marginalized_likelihood(node, data, dtype)
    scipy_obj, params = get_scipy_obj_params(node)
    probs[~marg_ids] = scipy_obj.pdf(observations, **params)
    return probs


def categorical_log_likelihood(node, data=None, dtype=np.float64, **kwargs):
    probs, marg_ids, observations = leaf_marginalized_likelihood(
        node, data, dtype, log_space=True
    )

    cat_data = observations.astype(np.int64)
    assert np.all(np.equal(np.mod(cat_data, 1), 0))
    out_domain_ids = cat_data >= node.k

    idx_out = ~marg_ids
    idx_out[idx_out] = out_domain_ids
    probs[idx_out] = 0

    idx_in = ~marg_ids
    idx_in[idx_in] = ~out_domain_ids
    probs[idx_in] = np.array(np.log(node.p))[cat_data[~out_domain_ids]]
    return probs


import numpy as np
from spn.algorithms.Inference import likelihood

node_uniform = Uniform()
print(node_uniform)

node_categorical = Categorical(p=[0.2, 0.3, 0.4, 0.1], scope=0)
print(node_categorical.p)
assign_ids(node_categorical)
rebuild_scopes_bottom_up(node_categorical)


node_gaussian = Gaussian(32, 2.5, scope=0)
assign_ids(node_gaussian)
rebuild_scopes_bottom_up(node_gaussian)
print(node_gaussian)
print("====s====")
data = np.array([[34], [32]])
result = continuous_likelihood(node_gaussian, data)
print(result)
result2 = likelihood(node_gaussian, data)
print(result2)
print("====2====")

# from spn.structure.leaves.parametric.Inference import (
#    categorical_dictionary_log_likelihood,
#    categorical_log_likelihood,
# )

data = np.array([[1]])
result = categorical_log_likelihood(node_categorical, data)
print(result)
result2 = likelihood(node_categorical, data)
print(result2)
print(np.log(result2))

# eval_spn_bottom_up(node_gaussian)

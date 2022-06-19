import numpy as np
import os
import csv
from spn.algorithms.Statistics import get_structure_stats

from spn.algorithms.StructureLearning import learn_structure


DEBD = [
    "accidents",
    "ad",
    "baudio",
    "bbc",
    "bnetflix",
    "book",
    "c20ng",
    "cr52",
    "cwebkb",
    "dna",
    "jester",
    "kdd",
    "kosarek",
    "msnbc",
    "msweb",
    "nltcs",
    "plants",
    "pumsb_star",
    "tmovie",
    "tretail",
]


DEBD_num_vars = {
    "accidents": 111,
    "ad": 1556,
    "baudio": 100,
    "bbc": 1058,
    "bnetflix": 100,
    "book": 500,
    "c20ng": 910,
    "cr52": 889,
    "cwebkb": 839,
    "dna": 180,
    "jester": 100,
    "kdd": 64,
    "kosarek": 190,
    "msnbc": 17,
    "msweb": 294,
    "nltcs": 16,
    "plants": 69,
    "pumsb_star": 163,
    "tmovie": 500,
    "tretail": 135,
}


DEBD_display_name = {
    "accidents": "accidents",
    "ad": "ad",
    "baudio": "audio",
    "bbc": "bbc",
    "bnetflix": "netflix",
    "book": "book",
    "c20ng": "20ng",
    "cr52": "reuters-52",
    "cwebkb": "web-kb",
    "dna": "dna",
    "jester": "jester",
    "kdd": "kdd-2k",
    "kosarek": "kosarek",
    "msnbc": "msnbc",
    "msweb": "msweb",
    "nltcs": "nltcs",
    "plants": "plants",
    "pumsb_star": "pumsb-star",
    "tmovie": "each-movie",
    "tretail": "retail",
}


def load_mnist(data_dir):
    """Load MNIST"""

    # save current random state
    state = np.random.get_state()
    np.random.seed(12345)

    # make train/validation split
    validation_frac = 0.1
    num_valid = max(int(round(60000 * validation_frac)), 1)
    rp = np.random.permutation(60000)
    valid_idx = sorted(rp[0:num_valid])
    train_idx = sorted(rp[num_valid:])

    # restore random state
    np.random.set_state(state)

    fd = open(os.path.join(data_dir, "train-images-idx3-ubyte"))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    train_x = loaded[16:].reshape((60000, 784)).astype(np.float32)

    fd = open(os.path.join(data_dir, "train-labels-idx1-ubyte"))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    train_labels = loaded[8:].reshape((60000)).astype(np.float32)

    fd = open(os.path.join(data_dir, "t10k-images-idx3-ubyte"))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    test_x = loaded[16:].reshape((10000, 784)).astype(np.float32)

    fd = open(os.path.join(data_dir, "t10k-labels-idx1-ubyte"))
    loaded = np.fromfile(file=fd, dtype=np.uint8)
    test_labels = loaded[8:].reshape((10000)).astype(np.float32)

    train_labels = np.asarray(train_labels)
    test_labels = np.asarray(test_labels)

    valid_x = train_x[valid_idx, :]
    valid_labels = train_labels[valid_idx]
    train_x = train_x[train_idx, :]
    train_labels = train_labels[train_idx]

    return train_x, train_labels, valid_x, valid_labels, test_x, test_labels


def load_debd(data_dir, name, dtype="int32"):
    """Load one of the twenty binary density esimtation benchmark datasets."""

    train_path = os.path.join(data_dir, "datasets", name, name + ".train.data")
    test_path = os.path.join(data_dir, "datasets", name, name + ".test.data")
    valid_path = os.path.join(data_dir, "datasets", name, name + ".valid.data")

    reader = csv.reader(open(train_path, "r"), delimiter=",")
    train_x = np.array(list(reader)).astype(dtype)

    reader = csv.reader(open(test_path, "r"), delimiter=",")
    test_x = np.array(list(reader)).astype(dtype)

    reader = csv.reader(open(valid_path, "r"), delimiter=",")
    valid_x = np.array(list(reader)).astype(dtype)

    return train_x, test_x, valid_x


import os
import tempfile
import urllib.request
import shutil
import subprocess
import pickle
import gzip
import numpy as np
import json

# import utils

# https://github.com/arranger1044/DEBD


def maybe_download_DEBD(data_dir):
    if os.path.isdir(data_dir):
        print("DEBD already exists")
        return
    subprocess.run(["git", "clone", "https://github.com/arranger1044/DEBD", data_dir])
    wd = os.getcwd()
    os.chdir(data_dir)
    subprocess.run(["git", "checkout", "80a4906dcf3b3463370f904efa42c21e8295e85c"])
    subprocess.run(["rm", "-rf", ".git"])
    os.chdir(wd)


from spn.algorithms.splitting.Base import split_data_by_clusters


def get_split_cols_random_partition(rand_gen, fail=0.6):
    def split_cols_random_partitions(local_data, ds_context, scope):
        if rand_gen.random_sample() < fail:
            return [(local_data, scope, 1.0)]

        clusters = np.zeros_like(scope)

        for i, new_scope in enumerate(np.array_split(np.argsort(scope), 2)):
            clusters[new_scope] = i

        return split_data_by_clusters(local_data, clusters, scope, rows=False)

    return split_cols_random_partitions


from joblib import Memory
from spn.algorithms.LearningWrappers import learn_classifier, learn_parametric
from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian
from spn.structure.Base import Context, get_nodes_by_type

memory = Memory("/tmp/cache", verbose=0, compress=9)


@memory.cache
def learn_spn_classifier(data, min_inst):
    spn_classification = learn_classifier(
        data,
        Context(parametric_types=[Categorical] + [Gaussian] * (28 * 28)).add_domains(
            data
        ),
        learn_parametric,
        0,
        cols=get_split_cols_random_partition(np.random.RandomState(17)),
        rows="kmeans",
        min_instances_slice=min_inst,
    )
    return spn_classification


from spn.structure.StatisticalTypes import MetaType
from spn.algorithms.Inference import log_likelihood
from spn.algorithms.Inference import likelihood


def learn_spn():
    data_dir = "/mnt/d/datasets/DEDB"
    maybe_download_DEBD(data_dir)
    train_x, test_x, valid_x = load_debd(data_dir, "nltcs")
    ds_context = Context(parametric_types=[Categorical] * train_x.shape[1])
    ds_context.add_domains(train_x)

    spn = learn_parametric(train_x, ds_context)

    return train_x, test_x, valid_x, spn


import tensorflow as tf
from spn.gpu.TensorFlow import (
    spn_to_tf_graph,
    eval_tf,
    likelihood_loss,
    tf_graph_to_spn,
)

tf = tf.compat.v1
tf.disable_v2_behavior()


def test_eval_gaussian():
    np.random.seed(17)
    data = (
        np.random.normal(10, 0.01, size=2000).tolist()
        + np.random.normal(30, 10, size=2000).tolist()
    )
    data = np.array(data).reshape((-1, 10))
    data = data.astype(np.float32)

    ds_context = Context(
        meta_types=[MetaType.REAL] * data.shape[1],
        parametric_types=[Gaussian] * data.shape[1],
    )

    spn = learn_parametric(data, ds_context)

    ll = log_likelihood(spn, data)

    tf_ll = eval_tf(spn, data)

    print(np.all(np.isclose(ll, tf_ll)))


def test_eval_nltcs():
    data_dir = "/mnt/d/datasets/DEDB"
    maybe_download_DEBD(data_dir)
    train_x, test_x, valid_x = load_debd(data_dir, "nltcs")
    ds_context = Context(parametric_types=[Categorical] * train_x.shape[1])
    ds_context.add_domains(train_x)

    spn = learn_parametric(train_x, ds_context)

    ll = log_likelihood(spn, train_x)
    print("xxxxxxxxxxx")
    print(ll)
    print("xxxxxxxxxxx")
    tf_ll = eval_tf(spn, train_x)
    print("xxxxxxxxxxx")
    print(tf_ll)
    print("xxxxxxxxxxx")

    print(np.all(np.isclose(ll, tf_ll)))


test_eval_nltcs()

train_x, test_x, valid_x, nltcs_spn = build_nltcs_spn()
like = likelihood(nltcs_spn, test_x)
print(like)

stats = get_structure_stats(nltcs_spn)
print(stats)

import numpy as np

np.random.seed(123)

from spn.algorithms.LearningWrappers import learn_parametric, learn_classifier
from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian
from spn.structure.Base import Context
import matplotlib.pyplot as plt

# import seaborn as sns

train_data = np.c_[
    np.r_[np.random.normal(5, 1, (500, 2)), np.random.normal(10, 1, (500, 2))],
    np.r_[np.zeros((500, 1)), np.ones((500, 1))],
]

# sns.scatterplot(train_data[:, 0], train_data[:, 1], hue=train_data[:, 2])
spn_classification = learn_classifier(
    train_data,
    Context(parametric_types=[Gaussian, Gaussian, Categorical]).add_domains(train_data),
    learn_parametric,
    2,
)

from spn.io.Graphics import draw_spn

draw_spn(spn_classification)

test_data = np.array([3.0, 4.0, np.nan, 12.0, 18.0, np.nan]).reshape(-1, 3)
print(test_data)
print(test_data.shape)
from spn.algorithms.MPE import mpe


print(spn_classification.parameters)
print(mpe(spn_classification, test_data))

import math
from numpy.lib.function_base import copy
from spn.structure.Base import eval_spn_bottom_up


from spn.io.Text import str_to_spn
from datetime import datetime


def read_spn_from_equationFile(filename):
    f = open(filename, "r")
    spnStr = f.read()
    spn = str_to_spn(spnStr)
    return spn


# import example_spn
# print(datetime.now().strftime("%H:%M:%S"))
# mnist_spn = read_spn_from_equationFile("mnist_spn.eq")
# print(datetime.now().strftime("%H:%M:%S"))


# image_of_2 = open("../2.png", "r")
# image_of_2.read()

from PIL import Image
import numpy as np


def convert(loaction):
    im = Image.open(loaction)
    px = im.load()
    result = []
    result.append(np.nan)
    for y in range(im.size[0]):
        for x in range(im.size[1]):
            coordinate = x, y
            r, g, b = im.getpixel(coordinate)
            singe_rep = (((r + g + b) / (255 * 3)) - 0.5) * 2.0
            # rounded = math.ceil(singe_rep)

            # print(f"{singe_rep} ", end="")
            result.append(singe_rep)
        # print("")
    return result


location = "2.png"
test_data = convert(location)


def gen_numpy_array_for_image(arr):
    two_d = (np.reshape(arr, (28, 28)) * 255).astype(np.uint8)
    # img = Image.fromarray(two_d, "L")
    return two_d  # img


# numpy_array_of_image = gen_numpy_array_for_image(my_im)
# print(numpy_array_of_image.shape)

# https://github.com/SPFlow/SPFlow/blob/master/src/spn/experiments/layers/mnist_test.py

train_data = []
test_data = []


def example_spn_mnist():
    from spn.experiments.layers.mnist_test import get_mnist_spn

    trainds, testds, spn, torch_spn = get_mnist_spn(200)
    train_data.append(np.array(trainds[0]))
    train_data.append(np.array(trainds[1]))
    train_data.append(np.array(trainds[2]))
    train_data.append(np.array(trainds[3]))
    train_data.append(np.array(trainds[4]))
    train_data.append(np.array(trainds[5]))
    train_data.append(np.array(trainds[6]))
    print(f"len tain: {len(trainds)}\t len of tesxt: {len(testds)}")

    test_data.append(np.array(testds[0]))
    test_data.append(np.array(testds[1]))
    test_data.append(np.array(testds[2]))
    test_data.append(np.array(testds[3]))
    test_data.append(np.array(testds[4]))
    test_data.append(np.array(testds[5]))
    test_data.append(np.array(testds[6]))

    test_datas = train_data + test_data

    f = open("data_for_mnist.in", "w")
    for index in range(6):
        for entry in list(np.array(trainds[index])):
            print(type(entry))
            f.write(f"{str(entry)} ")
        f.write("\n")

    for index in range(6):
        for entry in list(np.array(testds[index])):
            f.write(f"{str(entry)} ")
        f.write("\n")
    f.close()

    # print(f"trainds: {testds}")
    # print(f"trainds: {torch_spn}")
    return spn
    # write_spn_as_equationFile(spn, "mnist_spn.eq")
    # return read_spn_from_equationFile("mnist_spn.eq")


from spn.algorithms.Inference import log_likelihood
from spn.algorithms.Inference import likelihood
from spn.algorithms.MPE import mpe

spn = example_spn_mnist()
labels = []
for train_image in train_data:
    labels.append(train_image[0])
    train_image[0] = np.nan

# print(test_data[0])
for test_image in test_data:
    labels.append(test_image[0])
    test_image[0] = np.nan

# print(train_data)

test_datas = train_data + test_data

test_data_zero = []
for idx in range(10):
    zero_image_data = copy(test_datas[1])
    zero_image_data[0] = idx
    test_data_zero.append(zero_image_data)

test_data_one = []
for idx in range(10):
    one_image_data = copy(test_datas[3])
    one_image_data[0] = idx
    test_data_one.append(one_image_data)

test_datas_arr = np.array(test_data_zero + test_data_one)  # np.array(test_datas)

print(test_datas_arr.shape)
log_result = log_likelihood(spn, test_datas_arr)
print(log_result)
like_result = likelihood(spn, test_datas_arr)
print(like_result)
# mpe_results = mpe(spn, test_datas_arr)
# for index in range(len(mpe_results)):
#    print(f"should be: {labels[index]} was: {mpe_results[index][0]}")


# print(image_of_2.read())

f = open("mnist_tensor.in", "r")
mnist_tesnor = f.read()
mnist_tesnor = mnist_tesnor.replace("\n", "")
numbers = mnist_tesnor.split(",")
float_numbers = list(map(float, numbers))
label = float_numbers[0]


def vis(float_numbers):
    float_numbers = float_numbers[1:]
    # print(float_numbers)
    for x in range(28):
        for y in range(28):
            float_number = float_numbers[x * 28 + y]
            # float_number_rounded = round(float_number, 1)
            if float_number == 0.0:
                str_for_nummer = "0"
            if float_number > 0.1:
                str_for_nummer = "p"
            if float_number < -0.1:
                str_for_nummer = "n"
            if float_number == -1.0:
                str_for_nummer = "x"
            if float_number > -0.1 and float_number < 0.1:
                str_for_nummer = "z"
            print(f"{str_for_nummer} ", end="")

        print("")


vis(float_numbers)


from PIL import Image
import numpy as np
import math


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


print("======")
location = "2.png"
res = convert(location)
vis(res)

import math
import numpy as np


class ImgUitls:
    def __init__(self):
        pass

    @staticmethod
    def all_in_one(imgs):
        num = len(imgs)
        row = math.ceil(math.sqrt(num))
        column = row
        width, height, channel = imgs[0].shape
        all_in_one = np.ones((width * row, height * column, channel), dtype=np.uint8)
        for index, img in enumerate(imgs):
            a = index // row
            b = index % column
            all_in_one[a * width:(a + 1) * width, b * height: (b + 1) * height, :] = img
        return all_in_one


if __name__ == '__main__':
    pass

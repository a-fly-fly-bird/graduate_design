import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import time
import matplotlib as mpl
import seaborn as sns
import json


class ImgHeatMap:
    def __init__(self):
        # 根据时间生成随机数，保证每次都不一样
        np.random.seed(int(time.time()))
        self.fig, self.axes = plt.subplots()
        sns.set()

    def plot_heatmap(self, img, heatmap):
        print("Image shape", img. shape)
        normalized_heat_map = self.get_heatmap_array(img, heatmap)
        # 去除坐标轴
        self.axes.cla()
        self.axes.imshow(img)
        self.axes.imshow(255 * normalized_heat_map, alpha=0.8, cmap="viridis")
        self.axes.set_axis_off()
        plt.show()

    def get_heatmap_array(self, img, heat):
        height, width, _ = img.shape
        heat[:, 0] *= height
        heat[:, 1] *= width
        x = np.zeros((height, width))

        def count_heat(i):
            try:
                x[int(i[0]), int(i[1])] += 1
            except:
                pass
        # 必选参数：func,axis,arr。其中func是我们自定义的一个函数，函数func(arr)中的arr是一个数组，函数的主要功能就是对数组里的每一个元素进行变换，得到目标的结果。其中axis表示函数func对数组arr作用的轴。
        np.apply_along_axis(count_heat, axis=1, arr=heat)
        heat_map = ndimage.gaussian_filter(x, sigma=18)
        # 归一化
        max_value = np.max(heat_map)
        min_value = np.min(heat_map)
        normalized_heat_map = (heat_map - min_value) / (max_value - min_value)
        return normalized_heat_map


class GazeHeatMap:
    def __init__(self) -> None:
        np.random.seed(int(time.time()))
        self.fig, self.axes = plt.subplots()
        sns.set(style='darkgrid')

    def plot_heatmap(self, heatmap):
        print("Image shape", heatmap.shape)
        normalized_heat_map = self.get_heatmap_array(heatmap)
        # 坐标轴居中
        self.axes.spines['left'].set_position('center')
        self.axes.spines['bottom'].set_position('center')
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        
        self.axes.xaxis.set_ticks_position('bottom')
        self.axes.yaxis.set_ticks_position('left')

        sns.heatmap((255 * normalized_heat_map).astype(int), annot=False, fmt='d', linewidths=0, cmap="RdBu_r", center=125)
        self.axes = plt.gca()
        # plt.tick_params(axis='x',colors='red')
        # plt.tick_params(axis='y',colors='red')
        self.axes.axes.xaxis.set_ticks([])
        self.axes.axes.yaxis.set_ticks([])

        # plt.xlim((-21, 21))
        # plt.ylim((-21, 21))
        plt.grid(False)
        plt.show()

    def get_heatmap_array(self, gaze):
        max_value_pitch = np.max(gaze[:, 0])
        min_value_pitch = np.min(gaze[:, 0])
        print(max_value_pitch,' ', min_value_pitch)
        max_value_yaw = np.max(gaze[:, 1])
        min_value_yaw = np.min(gaze[:, 1])
        print(max_value_yaw, ' ', min_value_yaw)
        gaze.astype(np.int32)
        x = np.zeros((int(max_value_pitch - min_value_pitch) +
                     1, int(max_value_yaw - min_value_yaw) + 1))
        print(x.shape)
        def count_heat(i):
            try:
                print(int(i[0] - min_value_pitch), ' ', int(i[1] - min_value_yaw))
                x[int(i[0] - min_value_pitch), int(i[1] - min_value_yaw)] += 1
            except:
                pass
        # 必选参数：func,axis,arr。其中func是我们自定义的一个函数，函数func(arr)中的arr是一个数组，函数的主要功能就是对数组里的每一个元素进行变换，得到目标的结果。其中axis表示函数func对数组arr作用的轴。
        np.apply_along_axis(count_heat, axis=1, arr=gaze)
        print(x)
        heat_map = ndimage.gaussian_filter(x, sigma=5)
        print('heat map', heat_map)
        # 归一化
        max_value = np.max(heat_map)
        min_value = np.min(heat_map)
        normalized_heat_map = (heat_map - min_value) / (max_value - min_value)
        return normalized_heat_map


def main():
    heatMap = GazeHeatMap()
    # 0: black; 255: white
    # img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    # 假设有1000条数据, [0,1)内的随机数
    # heat = np.random.rand(1000, 2)
    # heat = np.random.uniform(-21, 21, (1000, 2))
    with open('/Users/lucas/Documents/School/大四下/毕业设计/5. gaze_whl/gaze_guy/gaze.json', 'r+') as f:
        data = json.load(f)
    gaze = np.asarray(data['direction'], dtype=np.float32)
    heatMap.plot_heatmap(gaze)


if __name__ == '__main__':
    main()

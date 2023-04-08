import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import time

class HeatMap:
    def __init__(self):
        np.random.seed(int(time.time()))
        self.fig, self.axes = plt.subplots()

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
    
def main():
    heatMap = HeatMap()
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    # 假设有1000条数据, [0,1)内的随机数
    heat = np.random.rand(1000, 2)
    heatMap.plot_heatmap(img, heat)

if __name__ == '__main__':
    main()
import math
import os

import cv2
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

    @staticmethod
    def image2video(img_dir, video_filepath, fps=1):
        if not os.path.exists(img_dir) or not os.path.exists(os.path.split(video_filepath)[0]):
            print("路径不存在，请先创建文件夹。")
        else:
            images = [img for img in os.listdir(img_dir) if img.endswith(('.png', '.jpg', 'jpeg', 'bmp'))]
            frame = cv2.imread(os.path.join(img_dir, images[0]))
            height, width, layers = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            videoWriter = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height), True)

            num = 0
            for image in images:
                num += 1
                videoWriter.write(cv2.imread(os.path.join(img_dir, image)))
                print(f"生成第{num}帧")
            cv2.destroyAllWindows()
            videoWriter.release()
            print('生成成功')
            return True

    @staticmethod
    def video2img(video_filepath, img_dir):
        if not os.path.exists(img_dir) or not os.path.exists(os.path.split(video_filepath)[0]):
            print("路径不存在，请先创建文件夹。")
        else:
            vidcap = cv2.VideoCapture(video_filepath)
            success, image = vidcap.read()
            count = 0
            while success:
                cv2.imwrite(os.path.join(img_dir, "frame%d.jpg" % count), image)  # save frame as JPEG file
                success, image = vidcap.read()
                print('Read a new frame: ', success)
                count += 1
            print("成功转成图片")


if __name__ == '__main__':
    video_path = r'/Users/lucas/Desktop/face.mp4'
    out_dir = r'/Users/lucas/Desktop/hello/'
    ImgUitls.video2img(video_path, out_dir)

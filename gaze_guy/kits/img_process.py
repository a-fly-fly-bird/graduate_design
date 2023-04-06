import math
import os
import time
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
    def video2img(video_filepath, img_dir, ratio):
        if isinstance(video_filepath, str):
            if not os.path.exists(img_dir) or not os.path.exists(os.path.split(video_filepath)[0]):
                print("路径不存在，请先创建文件夹。")
        else:
            cap = cv2.VideoCapture(video_filepath)
            fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
            print(fps)
            count = 0
            sleep_time = 1 / fps * ratio
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    filename = os.path.join(img_dir, 'frame{:d}.jpg'.format(count))
                    cv2.imwrite(filename, frame)
                    count += fps  # i.e. at 30 fps, this advances one second
                    print(f"保存{filename}成功")
                    time.sleep(sleep_time)
                else:
                    cap.release()
                    break
            print("成功转成图片")

    @staticmethod
    def get_available_cameras():
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr

    @staticmethod
    def keyShortcut(img_dir):
        cam = cv2.VideoCapture(1)
        cv2.namedWindow("key shortcut")
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("hello", frame)

            k = cv2.waitKey(1)  # 单位是ms
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = os.path.join(img_dir, 'frame{:d}.jpg'.format(img_counter))
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
        cam.release()
        cv2.destroyAllWindows()

# co-author
Chat GPT（听我说谢谢你😭）
# Run Env
Ubuntu 22.04

Known problem: OS X do not support UI on non main thread. So OS X can not run demos in `gaze_guy.web`. `gaze_guy.display` is fine.

## git clone

git clone 记得加 `--depth 1` 参数。不然会很大。
# __main__.py 

参考：[__main__ --- 最高层级代码环境](https://docs.python.org/zh-cn/3/library/__main__.html)

创建一个Python包时，需有一个`__init__.py`文件，用来标识Python包。

在命令行直接输入python -m package_name 就会执行__main__.py文件。

# face detector
Dlib是一个现代化的C++工具箱，其中包含用于在C++中创建复杂软件以解决实际问题的机器学习算法和工具。

MediaPipe 是一款由 Google Research 开发并开源的多媒体机器学习模型应用框架。基于图形的跨平台框架，用于构建多模式（视频，音频和传感器）应用的机器学习管道。

## 对比
* 都支持GPU加速
* dlib只支持2d坐标，mediapipe支持3d坐标
* mediapipe安装和使用更简单
* （貌似）mediapipe性能更好

# Kalman Filter
[filterpy](https://github.com/rlabbe/filterpy) 有 卡尔曼滤波的支持，因此不用自己实现。

或者kits的kalman里有师兄实现的kalman filter。
## @ operator

PEP 465 - A dedicated infix operator for matrix multiplication

可以理解为矩阵乘法操作符。

# 部署
实现了基于flask的和更底层的socket两种方案的c/s。flask的可以实现跨平台，通过浏览器访问。

# TODO

- [x] ~~threads seperate(client & server), 将server部署到学校的服务器。~~
- [ ] 根据注视比等参数进行分心识别
- [ ] fix & debug

# Helpful Command
```sh
# rm images or containers
docker rmi `docker images | grep "<none>" | awk '{print $3}'`
docker rm $(docker ps -a -q)
# export

# run
python -m  gaze_guy.display.main --video path/a.mp4 --output-dir ~/Downloads --ext mp4
```
https://python.plainenglish.io/real-time-image-processing-using-websockets-and-flask-in-python-and-javascript-97fb4a0a764f
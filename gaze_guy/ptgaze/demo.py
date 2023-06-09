from gaze_guy.kits.kalman import Kalman
import datetime
import logging
import pathlib
import time
from typing import Optional
import json
import cv2
import numpy as np
import os
from omegaconf import DictConfig

from PyQt6.QtCore import QThread, pyqtSignal

from gaze_guy.kits.distraction_judge import DistractionJudgement

from .common import Face, FacePartsName, Visualizer
from .gaze_estimator import GazeEstimator
from .utils import get_3d_face_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Demo(QThread):
    gazeEstimationSignal = pyqtSignal(np.ndarray)
    QUIT_KEYS = {27, ord('q')}

    def __init__(self, config: DictConfig):
        super().__init__()
        self._run_flag = True
        self.config = config
        self.gaze_estimator = GazeEstimator(config)
        face_model_3d = get_3d_face_model(config)
        self.visualizer = Visualizer(self.gaze_estimator.camera,
                                     face_model_3d.NOSE_INDEX)

        self.cap = self._create_capture()
        self.output_dir = self._create_output_dir()
        self.writer = self._create_video_writer()

        self.cnt = 0
        self.dates = None
        self.stop = False
        self.show_bbox = self.config.demo.show_bbox
        self.show_head_pose = self.config.demo.show_head_pose
        self.show_landmarks = self.config.demo.show_landmarks
        self.show_normalized_image = self.config.demo.show_normalized_image
        self.show_template_model = self.config.demo.show_template_model

        self.my_kalman_filter = Kalman()
        self.distractionJudgement = DistractionJudgement()
        self.gaze_vector = {
            "record_time": None,
            "data": []
        }
        filename = '/Users/lucas/Documents/School/大四下/毕业设计/5. code/gaze_whl/dates.json'
        with open(filename,'r') as file_object:
            self.dates = json.load(file_object)

    def run(self) -> None:
        if self.config.demo.use_camera or self.config.demo.video_path:
            self._run_on_video()
        elif self.config.demo.image_path:
            self._run_on_image()
        else:
            raise ValueError

    def stop_thread(self):
        """Sets run flag to False and waits for thread to finish"""
        print('停止运行，开始输出日志记录')
        f_path = os.path.join(os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))), 'gaze.json')
        print(f_path)
        with open(f_path, 'w') as f:
            f.write(json.dumps(self.gaze_vector))
        print('输出日志记录完成')
        self._run_flag = False

    def _run_on_image(self):
        image = cv2.imread(self.config.demo.image_path)
        self._process_image(image)
        if self.config.demo.display_on_screen:
            while True:
                key_pressed = self._wait_key()
                if self.stop:
                    break
                if key_pressed:
                    self._process_image(image)
                # cv2.imshow('image', self.visualizer.image)
        if self.config.demo.output_dir:
            name = pathlib.Path(self.config.demo.image_path).name
            output_path = pathlib.Path(self.config.demo.output_dir) / name
            cv2.imwrite(output_path.as_posix(), self.visualizer.image)

    def _run_on_video(self) -> None:
        self.gaze_vector['record_time'] = time.strftime(
            "%a %b %d %H:%M:%S %Y", time.localtime())
        self.gaze_vector['data'].append({
            'date': self.dates[self.cnt],
            'gaze': [0, 0],
            # 'distracted': 'true',
            # 'distracted_time': 0,
            # 'timestamp': time.time()
        })
        self.cnt += 1
        while True:
            begin = time.time()
            if self.config.demo.display_on_screen:
                self._wait_key()
                if self.stop:
                    break

            ok, frame = self.cap.read()
            if not ok:
                break
            self._process_image(frame)

            if self.config.demo.display_on_screen:
                now_data = self.gaze_vector['data'][-1]
                end = time.time()
                fps = 1 / (end - begin)
                fps_s = f'FPS: {fps:.2f}'
                # https://blog.csdn.net/u013685264/article/details/121661895
                cv_img_copy = self.visualizer.image.copy()
                cv2.rectangle(cv_img_copy, pt1=(100, 75), pt2=(
                    550, 400), color=(0, 0, 255), thickness=3)
                cv2.putText(cv_img_copy, fps_s, (40, 40),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 200, 200), 1)
                # if now_data['distracted']:
                #     cv2.putText(cv_img_copy, f'Distraction, {now_data["distracted_time"]}', (
                #         300, 300), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 2)
                # else:
                #     cv2.putText(cv_img_copy, f'Driving, {now_data["distracted_time"]}', (
                #         300, 300), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 2)
                self.gazeEstimationSignal.emit(cv_img_copy)
            f_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'gaze.json')
            with open(f_path, 'w') as f:
                f.write(json.dumps(self.gaze_vector))
        self.cap.release()
        if self.writer:
            self.writer.release()

    def _process_image(self, image) -> None:
        undistorted = cv2.undistort(
            image, self.gaze_estimator.camera.camera_matrix,
            self.gaze_estimator.camera.dist_coefficients)

        self.visualizer.set_image(image.copy())
        faces = self.gaze_estimator.detect_faces(undistorted)
        if faces:
            for face in faces:
                self.gaze_estimator.estimate_gaze(undistorted, face)
                self._draw_face_bbox(face)
                self._draw_head_pose(face)
                self._draw_landmarks(face)
                self._draw_face_template_model(face)
                self._draw_gaze_vector(face)
                self._display_normalized_image(face)
        else:
            self.gaze_vector['data'].append(
                self.distractionJudgement.judge_by_area((12345, 12345)))

        if self.config.demo.use_camera:
            self.visualizer.image = self.visualizer.image[:, ::-1]
        if self.writer:
            self.writer.write(self.visualizer.image)

    def _create_capture(self) -> Optional[cv2.VideoCapture]:
        if self.config.demo.image_path:
            return None
        if self.config.demo.use_camera:
            cap = cv2.VideoCapture(0)
        elif self.config.demo.video_path:
            cap = cv2.VideoCapture(self.config.demo.video_path)
        else:
            raise ValueError
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.gaze_estimator.camera.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.gaze_estimator.camera.height)
        return cap

    def _create_output_dir(self) -> Optional[pathlib.Path]:
        if not self.config.demo.output_dir:
            return
        output_dir = pathlib.Path(self.config.demo.output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        return output_dir

    @staticmethod
    def _create_timestamp() -> str:
        dt = datetime.datetime.now()
        return dt.strftime('%Y%m%d_%H%M%S')

    def _create_video_writer(self) -> Optional[cv2.VideoWriter]:
        if self.config.demo.image_path:
            return None
        if not self.output_dir:
            return None
        ext = self.config.demo.output_file_extension
        if ext == 'mp4':
            fourcc = cv2.VideoWriter_fourcc(*'H264')
        elif ext == 'avi':
            fourcc = cv2.VideoWriter_fourcc(*'PIM1')
        else:
            raise ValueError
        if self.config.demo.use_camera:
            output_name = f'{self._create_timestamp()}.{ext}'
        elif self.config.demo.video_path:
            name = pathlib.Path(self.config.demo.video_path).stem
            output_name = f'{name}.{ext}'
        else:
            raise ValueError
        output_path = self.output_dir / output_name
        writer = cv2.VideoWriter(output_path.as_posix(), fourcc, 30,
                                 (self.gaze_estimator.camera.width,
                                  self.gaze_estimator.camera.height))
        if writer is None:
            raise RuntimeError
        return writer

    def _wait_key(self) -> bool:
        key = cv2.waitKey(self.config.demo.wait_time) & 0xff
        if key in self.QUIT_KEYS:
            self.stop = True
        elif key == ord('b'):
            self.show_bbox = not self.show_bbox
        elif key == ord('l'):
            self.show_landmarks = not self.show_landmarks
        elif key == ord('h'):
            self.show_head_pose = not self.show_head_pose
        elif key == ord('n'):
            self.show_normalized_image = not self.show_normalized_image
        elif key == ord('t'):
            self.show_template_model = not self.show_template_model
        else:
            return False
        return True

    def _draw_face_bbox(self, face: Face) -> None:
        if not self.show_bbox:
            return
        self.visualizer.draw_bbox(face.bbox)

    def _draw_head_pose(self, face: Face) -> None:
        if not self.show_head_pose:
            return
        # Draw the axes of the model coordinate system
        length = self.config.demo.head_pose_axis_length
        self.visualizer.draw_model_axes(face, length, lw=2)

        euler_angles = face.head_pose_rot.as_euler('XYZ', degrees=True)
        pitch, yaw, roll = face.change_coordinate_system(euler_angles)
        logger.info(f'[head] pitch: {pitch:.2f}, yaw: {yaw:.2f}, '
                    f'roll: {roll:.2f}, distance: {face.distance:.2f}')

    def _draw_landmarks(self, face: Face) -> None:
        if not self.show_landmarks:
            return
        self.visualizer.draw_points(face.landmarks,
                                    color=(0, 255, 255),
                                    size=1)

    def _draw_face_template_model(self, face: Face) -> None:
        if not self.show_template_model:
            return
        self.visualizer.draw_3d_points(face.model3d,
                                       color=(255, 0, 525),
                                       size=1)

    def _display_normalized_image(self, face: Face) -> None:
        if not self.config.demo.display_on_screen:
            return
        if not self.show_normalized_image:
            return
        if self.config.mode == 'MPIIGaze':
            reye = face.reye.normalized_image
            leye = face.leye.normalized_image
            normalized = np.hstack([reye, leye])
        elif self.config.mode in ['MPIIFaceGaze', 'ETH-XGaze']:
            normalized = face.normalized_image
        else:
            raise ValueError
        if self.config.demo.use_camera:
            normalized = normalized[:, ::-1]
        cv2.imshow('normalized', normalized)

    def _draw_gaze_vector(self, face: Face) -> None:
        length = self.config.demo.gaze_visualization_length
        if self.config.mode == 'MPIIGaze':
            for key in [FacePartsName.REYE, FacePartsName.LEYE]:
                eye = getattr(face, key.name.lower())
                self.visualizer.draw_3d_line(
                    eye.center, eye.center + length * eye.gaze_vector)
                pitch, yaw = np.rad2deg(eye.vector_to_angle(eye.gaze_vector))
                logger.info(
                    f'[{key.name.lower()} 未滤波的结果:] pitch: {pitch:.2f}, yaw: {yaw:.2f}')

                # kalman filter module begin
                after = self.my_kalman_filter.predict_and_update([pitch, yaw])
                (pitch, yaw) = [float(i) for i in after][:2]
                logger.info(
                    f'[{key.name.lower()} 滤波后的结果:] pitch: {pitch:.2f}, yaw: {yaw:.2f}')
                # kalman filter module end
                self.gaze_vector['data'].append(
                    self.distractionJudgement.judge_by_area((pitch, yaw)))

        elif self.config.mode in ['MPIIFaceGaze', 'ETH-XGaze']:
            self.visualizer.draw_3d_line(
                face.center, face.center + length * face.gaze_vector)
            pitch, yaw = np.rad2deg(face.vector_to_angle(face.gaze_vector))
            logger.info(f'[face] pitch: {pitch:.2f}, yaw: {yaw:.2f}')
        else:
            raise ValueError

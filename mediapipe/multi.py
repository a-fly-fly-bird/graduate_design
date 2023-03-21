import cv2
import mediapipe as mp
import numpy as np
import math
from plane_filting import all

class MediaPipe:
    def __init__(self, cam_num):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_holistic = mp.solutions.holistic
        self.mp_objectron = mp.solutions.objectron
        self.mp_face_mesh = mp.solutions.face_mesh
        self.cap = cv2.VideoCapture(cam_num)
        self.imgs = []
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.BG_COLOR = (192, 192, 192)

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
    def get_landmark_coordinate(results_multi_face_landmarks):
        # https://stackoverflow.com/questions/67141844/python-how-to-get-face-mesh-landmarks-coordinates-in-mediapipe
        landmark = results_multi_face_landmarks[0].landmark
        return landmark

    def hostile(self):
        with self.mp_holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as holistic, \
                self.mp_objectron.Objectron(
                    static_image_mode=False,
                    max_num_objects=5,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.99,
                    model_name='Shoe') as objectron, \
                self.mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as face_mesh, \
                self.mp_selfie_segmentation.SelfieSegmentation(
                    model_selection=1) as selfie_segmentation:

            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results1 = holistic.process(image)
                results2 = objectron.process(image)
                results3 = face_mesh.process(image)
                results4 = selfie_segmentation.process(image)

                # Draw landmark annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                image2 = image.copy()
                image3 = image.copy()

                self.mp_drawing.draw_landmarks(
                    image,
                    results1.face_landmarks,
                    self.mp_holistic.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                self.mp_drawing.draw_landmarks(
                    image,
                    results1.pose_landmarks,
                    self.mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles
                        .get_default_pose_landmarks_style())
                # Flip the image horizontally for a selfie-view display.
                # cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
                # if cv2.waitKey(5) & 0xFF == 27:
                #     break

                if results2.detected_objects:
                    for detected_object in results2.detected_objects:
                        self.mp_drawing.draw_landmarks(
                            image2, detected_object.landmarks_2d, self.mp_objectron.BOX_CONNECTIONS)
                        self.mp_drawing.draw_axis(image2, detected_object.rotation,
                                                  detected_object.translation)
                if results3.multi_face_landmarks:
                    all(MediaPipe.get_landmark_coordinate(results3.multi_face_landmarks))
                    for face_landmarks in results3.multi_face_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image=image3,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing_styles
                                .get_default_face_mesh_tesselation_style())
                        self.mp_drawing.draw_landmarks(
                            image=image3,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing_styles
                                .get_default_face_mesh_contours_style())
                        self.mp_drawing.draw_landmarks(
                            image=image3,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_IRISES,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.mp_drawing_styles
                                .get_default_face_mesh_iris_connections_style())

                condition = np.stack(
                    (results4.segmentation_mask,) * 3, axis=-1) > 0.1
                bg_image = None
                if bg_image is None:
                    bg_image = np.zeros(image.shape, dtype=np.uint8)
                    bg_image[:] = self.BG_COLOR
                image4 = np.where(condition, image, bg_image)
                self.imgs.append(image)
                self.imgs.append(image2)
                self.imgs.append(image3)
                self.imgs.append(image4)

                all_in_one = MediaPipe.all_in_one(self.imgs)
                print(all_in_one.shape)
                print(all_in_one)
                # cv2.imshow("mutil_pic", np.hstack(self.imgs))
                cv2.imshow("main", all_in_one)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
                self.imgs.clear()


def main():
    mdp = MediaPipe(1)
    # img = np.ones((400, 400, 3))
    # four2one([img, img.copy()], 2)
    mdp.hostile()


if __name__ == '__main__':
    main()

import cv2
import mediapipe as mp
import numpy as np
import time

from utils import ImgUitls

"""
Mediapipe Homepage: https://google.github.io/mediapipe/getting_started/python

Args:
    image: A three channel BGR image represented as numpy ndarray.
    landmark_list: A normalized landmark list proto message to be annotated on
      the image.
    connections: A list of landmark index tuples that specifies how landmarks to
      be connected in the drawing.
    landmark_drawing_spec: Either a DrawingSpec object or a mapping from hand
      landmarks to the DrawingSpecs that specifies the landmarks' drawing
      settings such as color, line thickness, and circle radius. If this
      argument is explicitly set to None, no landmarks will be drawn.
    connection_drawing_spec: Either a DrawingSpec object or a mapping from hand
      connections to the DrawingSpecs that specifies the connections' drawing
      settings such as color and line thickness. If this argument is explicitly
      set to None, no landmark connections will be drawn.

比如connections=self.mp_face_mesh.FACEMESH_TESSELATION,在https://github.com/google/mediapipe/blob
/33d683c67100ef3db37d9752fcf65d30bea440c4/mediapipe/python/solutions/face_mesh_connections.py里面。
内容格式如下：
FACEMESH_LEFT_EYE = frozenset([(263, 249), (249, 390), (390, 373), (373, 374),
                               (374, 380), (380, 381), (381, 382), (382, 362),
                               (263, 466), (466, 388), (388, 387), (387, 386),
                               (386, 385), (385, 384), (384, 398), (398, 362)])
"""


class FaceMesh:
    def __init__(self, mp_drawing, mp_drawing_styles):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp_drawing
        self.mp_drawing_styles = mp_drawing_styles
        self.face_mesh_ = self.mp_face_mesh.FaceMesh(
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def face_mesh(self, image):
        drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        # with self.mp_face_mesh.FaceMesh(
        #         max_num_faces=2,
        #         refine_landmarks=True,
        #         min_detection_confidence=0.5,
        #         min_tracking_confidence=0.5) as face_mesh:

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh_.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())
        # Flip the image horizontally for a selfie-view display.
        return cv2.flip(image, 1)

    def __del__(self):
        self.face_mesh_.close()


class Hands:
    def __init__(self, mp_drawing, mp_drawing_styles):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp_drawing
        self.mp_drawing_styles = mp_drawing_styles
        self.hands_ = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def hands(self, image):
        # with self.mp_hands.Hands(
        #         model_complexity=0,
        #         min_detection_confidence=0.5,
        #         min_tracking_confidence=0.5) as hands:
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands_.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        return (cv2.flip(image, 1))

    def __del__(self):
        self.hands_.close()


class Selfie:
    def __init__(self, mp_drawing, mp_drawing_styles):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.mp_drawing = mp_drawing
        self.mp_drawing_styles = mp_drawing_styles
        self.selfie_segmentation_ = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=1)

    def selfie(self, image, BG_COLOR=(192, 192, 192)):
        # with self.mp_selfie_segmentation.SelfieSegmentation(
        #         model_selection=1) as selfie_segmentation:
        bg_image = None

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = self.selfie_segmentation_.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw selfie segmentation on the background image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > 0.1
        # The background can be customized.
        #   a) Load an image (with the same width and height of the input image) to
        #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
        #   b) Blur the input image by applying image filtering, e.g.,
        #      bg_image = cv2.GaussianBlur(image,(55,55),0)
        if bg_image is None:
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
        output_image = np.where(condition, image, bg_image)

        return output_image

    def __del__(self):
        self.selfie_segmentation_.close()


class Holistic:
    def __init__(self, mp_drawing, mp_drawing_styles):
        self.mp_drawing = mp_drawing
        self.mp_drawing_styles = mp_drawing_styles
        self.mp_holistic = mp.solutions.holistic
        self.holistic_ = self.mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def holistic(self, image):
        # with self.mp_holistic.Holistic(
        #         min_detection_confidence=0.5,
        #         min_tracking_confidence=0.5) as holistic:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.holistic_.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            self.mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing_styles
                .get_default_face_mesh_contours_style())
        self.mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            self.mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles
                .get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        return (cv2.flip(image, 1))

    def __del__(self):
        self.holistic_.close()


class HeadPoseEstimation:
    def __init__(self, mp_drawing, mp_drawing_styles):
        self.mp_drawing = mp_drawing
        self.mp_drawing_styles = mp_drawing_styles
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh_ = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def head_pose_estimation(self, image):
        start = time.time()

        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False

        # Get the result
        results = self.face_mesh_.process(image)

        # To improve performance
        image.flags.writeable = True

        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])

                        # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                # The distortion parameters
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                # See where the user's head tilting
                if y < -10:
                    text = "Looking Left"
                elif y > 10:
                    text = "Looking Right"
                elif x < -10:
                    text = "Looking Down"
                elif x > 10:
                    text = "Looking Up"
                else:
                    text = "Forward"

                # Display the nose direction
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                cv2.line(image, p1, p2, (255, 0, 0), 3)

                # Add the text on the image
                cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                cv2.putText(image, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            end = time.time()
            totalTime = end - start

            fps = 1 / totalTime
            # print("FPS: ", fps)

            cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            self.mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)
        return image


def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    face_mesh = FaceMesh(mp_drawing, mp_drawing_styles)
    hands = Hands(mp_drawing, mp_drawing_styles)
    selfie = Selfie(mp_drawing, mp_drawing_styles)
    holistic = Holistic(mp_drawing, mp_drawing_styles)
    pose_estimation = HeadPoseEstimation(mp_drawing, mp_drawing_styles)

    cap = cv2.VideoCapture(1)

    while cap.isOpened():
        success, image = cap.read()
        img1 = pose_estimation.head_pose_estimation(image.copy())
        img2 = hands.hands(image.copy())
        img3 = selfie.selfie(image.copy())
        img4 = holistic.holistic(image.copy())
        imgs = [img1, img2, img3, img4]
        all_in_one = ImgUitls.all_in_one(imgs)
        cv2.imshow("main", all_in_one)
        if cv2.waitKey(5) & 0xFF == 27:
            break


if __name__ == '__main__':
    main()

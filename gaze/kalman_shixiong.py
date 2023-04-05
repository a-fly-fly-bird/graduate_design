import json

import numpy as np


class KalmanFilter:
    """
    Simple Kalman filter
    """

    def __init__(self, X, F, Q, Z, H, R, P, B=np.array([0]), M=np.array([0])):
        """
        Initialise the filter
        Args:
            X: State estimate
            P: Estimate covariance
            F: State transition model
            B: Control matrix
            M: Control vector
            Q: Process noise covariance
            Z: Measurement of the state X
            H: Observation model
            R: Observation noise covariance
        """
        self.X = X
        self.P = P
        self.F = F
        self.B = B
        self.M = M
        self.Q = Q
        self.Z = Z
        self.H = H
        self.R = R

    def predict(self):
        """
        Predict the future state
        Args:
            self.X: State estimate
            self.P: Estimate covariance
            self.B: Control matrix
            self.M: Control vector
        Returns:
            updated self.X
        """
        # Project the state ahead
        self.X = self.F @ self.X + self.B @ self.M
        self.P = self.F @ self.P @ self.F.T + self.Q

        return self.X

    def correct(self, Z):
        """
        Update the Kalman Filter from a measurement
        Args:
            self.X: State estimate
            self.P: Estimate covariance
            Z: State measurement
        Returns:
            updated X
        """
        K = self.P @ self.H.T @ inv(self.H @ self.P @ self.H.T + self.R)
        self.X += K @ (Z - self.H @ self.X)
        self.P = self.P - K @ self.H @ self.P

        return self.X

    def set_calibration_img(self, img_path):
        self.cabin_img_path = img_path

    def init_kalman(self):
        stateMatrix = np.zeros((4, 1), np.float32)  # [x,y,delta_x,delta_y]
        estimateCovariance = np.eye(stateMatrix.shape[0])
        transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        processNoiseCov = np.array([
            [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.001
        measurementStateMatrix = np.zeros((2, 1), np.float32)
        observationMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.01
        self.kalman = KalmanFilter(X=stateMatrix,
                                   P=estimateCovariance,
                                   F=transitionMatrix,
                                   Q=processNoiseCov,
                                   Z=measurementStateMatrix,
                                   H=observationMatrix,
                                   R=measurementNoiseCov)

        uSeAI = False
        latestaaze = None
        obj = json.loads(data)
        current_measurement = np.array([[float(obj['pitch'])], [float(obj['yaw'])]])
        current_prediction = self.kalman.predict()
        self.kalman.correct(current_measurement)

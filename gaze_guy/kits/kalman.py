from operator import inv
import numpy as np

from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise


class Kalman:
    def __init__(self):
        self.my_filter = KalmanFilter(dim_x=4, dim_z=2)
        self.init()

    def init(self):
        # initial state (location and velocity)
        self.my_filter.x = np.zeros((4, 1), dtype=np.float32)
        # covariance matrix
        self.my_filter.P = np.eye(self.my_filter.x.shape[0])
        self.my_filter.F = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [
                                    0, 0, 0, 1]], np.float32)    # state transition matrix
        # self.my_filter.Q = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32)  # process uncertainty
        self.my_filter.Q = Q_discrete_white_noise(dim=4, dt=0.1, var=0.1)
        # control transition matrix
        self.my_filter.Z = np.array([[1, 0], [0, 1]], dtype=np.float32)*0.001
        self.my_filter.H = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)    # Measurement function
        # state uncertainty
        self.my_filter.R = np.array([[1, 0], [0, 1]], dtype=np.float32)*0.01

    def predict(self, current_measurement):
        # while True:
        self.my_filter.predict()
        self.my_filter.update(current_measurement)
        # do something with the output
        x = self.my_filter.x
        return x[:2]

class OldKalmanFilter:
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
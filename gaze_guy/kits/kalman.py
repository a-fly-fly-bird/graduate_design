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

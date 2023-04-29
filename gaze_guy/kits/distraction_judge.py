import time
import numpy as np
import json

class DistractionJudgement:
    def __init__(self):
        self.distraction = False
        self.distraction_count = 0
        self.distraction_threshold = 2 # seconds
        self.distraction_duration = 0
        self.cnt = 0
        self.dates = None
        # self.distraction_duration_threshold = 1.0
        # self.distraction_duration_count = 0
        # self.distraction_duration_threshold_count = 5
        filename = '/Users/lucas/Documents/School/大四下/毕业设计/5. code/gaze_whl/dates.json'
        with open(filename,'r') as file_object:
            self.dates = json.load(file_object)
    
    def judge_by_area(self, gaze):
        # if not (abs(gaze[0]) < 10 and abs(gaze[1]) < 10):
        #     self.distraction_count += 1
        #     self.distraction_duration += 1
        # else:
        #     self.distraction_count = 0
        # if self.distraction_count > self.distraction_threshold * 30:
        #     self.distraction = True
        # else:
        #     self.distraction = False
        return self.record_res(gaze)
    
    def record_res(self, gaze):
        data = {}
        data['date'] = self.dates[self.cnt // 2]
        self.cnt += 1
        data['gaze'] = gaze
        # data['distracted'] = self.distraction
        # data['distracted_time'] = int(self.distraction_count / 30)
        # data['distraction_duration'] = self.distraction_duration
        # data['timestamp'] = time.time()
        return data

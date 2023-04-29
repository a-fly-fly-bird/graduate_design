import json
import os

path = '/Users/lucas/Documents/School/大四下/毕业设计/5. code/gaze_whl/gaze_guy/gaze.json'
with open(path, 'r+') as f:
    j_f = json.load(f)

datas = j_f['data'][1::2]

final = []

for data in datas:
    data = {
        'date': data['date'],
        'x': data['gaze'][0],
        'y': data['gaze'][1]
    }
    final.append(data)

f_path = os.path.join(os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))), 'final_data.json')
with open(f_path, 'w') as f:
        f.write(json.dumps(final))
#!/bin/zsh
rm -rf ./build ./dist ./gaze/egg-info
python setup.py bdist_wheel
cd dist
pip uninstall gaze -y
pip install ./gaze-0.1.0-py2.py3-none-any.whl
gaze --mode mpiigaze
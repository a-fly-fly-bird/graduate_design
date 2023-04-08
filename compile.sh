#!/bin/zsh

case "$1" in
  "build")
  rm -rf ./build ./dist ./gaze/egg-info
  python setup.py bdist_wheel
  ;;
  "install")
  pip uninstall gaze_guy -y
  pip install dist/gaze_guy-1.0.0-py2.py3-none-any.whl
  ;;
  "run")
  gaze_guy --mode mpiigaze
  ;;
esac

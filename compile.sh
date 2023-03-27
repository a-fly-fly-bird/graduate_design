#!/bin/zsh

case "$1" in
  "build")
  rm -rf ./build ./dist ./gaze/egg-info
  python setup.py bdist_wheel
  ;;
  "install")
  pip uninstall gaze -y
  # pip install ./gaze-0.2.0-py2.py3-none-any.whl
  pip install "$2"
  ;;
  "run")
  gaze --mode mpiigaze
  ;;
esac

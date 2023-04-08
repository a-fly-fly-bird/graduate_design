#!/bin/bash

for file in $1/*
do
    if [ -d "$file" ]
    then
        # img process
        echo "dir $file"
        mkdir "$file/video"
        ffmpeg -framerate 10 -pattern_type glob -i "$file/face_img/*.jpg" "$file/video/face_img.mp4"
        ffmpeg -framerate 10 -pattern_type glob -i "$file/lane_img/*.jpg" "$file/video/lane_img.mp4"
    fi
done

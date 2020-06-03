#!/bin/bash

trap 'sudo modprobe -r v4l2loopback' EXIT

sudo modprobe v4l2loopback video_nr=2 exclusive_caps=1 card_label="Generic USB2.0 Camera"

while true
do
    python3 switcher.py "$1" | ffmpeg -r 10 -f rawvideo -pixel_format bgr24 -video_size 1280x720 -i pipe:0 -metadata major_brand="isom" -metadata minor_version="512" -metadata compatible_brands="isomiso2avc1mp41" -filter:v "format=yuyv422" -f v4l2 /dev/video2
done
#python3 switcher.py "$1" | ffmpeg -r 10 -f rawvideo -pixel_format bgr24 -video_size 1280x720 -i pipe:0 -pixel_format yuv420p deneme.mp4
#python3 switcher.py "$1" | ffplay -f rawvideo -pixel_format bgr24 -video_size 1280x720 -i - 


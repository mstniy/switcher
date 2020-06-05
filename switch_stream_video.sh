#!/bin/bash

trap 'sudo modprobe -r v4l2loopback' EXIT

sudo modprobe v4l2loopback video_nr=2 exclusive_caps=1 card_label="Generic USB2.0 Camera"

while true
do
    python3 switcher.py "$1" | ffmpeg -r 10 -f rawvideo -pixel_format bgr24 -video_size 1280x720 -i pipe:0 -filter:v "format=yuyv422" -f v4l2 /dev/video2
    #python3 switcher.py "$1" | ffmpeg -r 10 -f rawvideo -pixel_format bgr24 -video_size 1280x720 -i pipe:0 -b:v 1M -vcodec mpeg4 -f mpegts udp://127.0.0.1:23000
    #python3 switcher.py "$1" | ffmpeg -r 10 -f rawvideo -pixel_format bgr24 -video_size 1280x720 -i pipe:0 deneme.mp4
done 


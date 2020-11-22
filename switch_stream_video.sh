#!/bin/bash

# The command line argument "cam" emulates a camera.

if [ "$1" = "cam" -o "$1" = "receive" ]
then
    trap 'sudo modprobe -r v4l2loopback' EXIT
    sudo modprobe v4l2loopback video_nr=2 exclusive_caps=1 card_label="Generic USB2.0 Camera"
fi

while true
do
    if [ "$1" = "cam" ]
    then
      python3 switcher.py | ffmpeg -re -f rawvideo -pixel_format bgr24 -video_size 640x480 -i pipe:0 -filter:v "format=yuyv422" -f v4l2 /dev/video2
    elif [ "$1" = "broadcast" ]
    then
      python3 switcher.py | ffmpeg -re -f rawvideo -pixel_format bgr24 -video_size 640x480 -i pipe:0 -b:v 1M -vcodec mpeg4 -tune zerolatency -f mpegts udp://127.0.0.1:23000
    elif [ "$1" = "receive" ]
    then
      ffmpeg -i udp://@:23000 -filter:v "format=yuyv422" -f v4l2 /dev/video2
    elif [ "$1" = "file" ]
    then
      python3 switcher.py | ffmpeg -re -f rawvideo -pixel_format bgr24 -video_size 640x480 -i pipe:0 deneme.mp4
    else
      echo "Unknown command."
      exit 1
    fi
done 


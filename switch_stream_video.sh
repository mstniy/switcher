#!/bin/bash

# The command line argument "cam" emulates a camera.

function cleanup {
    sudo modprobe -r v4l2loopback

    read -p "Allow raw cam access? [Y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
       sudo setfacl -m u:$USERNAME:rw- /dev/video0
    fi

    sudo setfacl -x u:switcher_user /dev/video0
    xhost -local:switcher_user
    sudo userdel switcher_user
}

if [ "$1" = "cam" -o "$1" = "receive" ]
then
    trap 'cleanup' EXIT
    # Load the virtual camera
    sudo modprobe v4l2loopback video_nr=2 exclusive_caps=1 card_label="Generic USB2.0 Camera"
    # Block access to the physical camera
    sudo setfacl -x u:$USERNAME /dev/video0
    # Create a dummy account that has access to the physical camera
    sudo useradd -r -s /bin/false switcher_user
    sudo setfacl -m u:switcher_user:rw- /dev/video0
    xhost local:switcher_user
fi

trap exit SIGINT

while true
do
    if [ "$1" = "cam" ]
    then
      # Run switcher.py as switcher_user, because it needs to be able to read from the physical camera
      sudo -u switcher_user python3 switcher.py | ffmpeg -re -f rawvideo -pixel_format bgr24 -video_size 640x480 -i pipe:0 -filter:v "format=yuyv422" -f v4l2 /dev/video2
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


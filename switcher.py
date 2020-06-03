import cv2
import sys
import time

def vcopen(arg):
	cap = cv2.VideoCapture(arg)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
	return cap

def boomerang(arr):
    idx=len(arr)
    dir=-1
    while True:
        idx += dir
        if idx < 0:
            idx = 0
            dir = 1
        if idx >= len(arr):
            idx = len(arr)-1
            dir = -1
        yield arr[idx]

MAX_AD_LENGTH = 60 # Seconds
TRANSITION_LENGTH = 0.10 # seconds

def main(argv):
	cap = vcopen(0)
	cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
	#cap.grab() # Force start the camera
	show_ad = 0
	ad_frames = []
	ad_last_read = 0
	ad_boomerang = None
	fps = cap.get(cv2.CAP_PROP_FPS)
	transition_frame = None
	transition_frames_left = 0
	transition_frame_count = 0
	while True:

		key = cv2.waitKey(33)
		if key==27:
			print('Switching...', file=sys.stderr)
			if show_ad == 0:
				show_ad = 1
				ad_boomerang = boomerang(ad_frames)
			else:
				show_ad = 0
				transition_frame = next(ad_boomerang)
				ad_frames = []
				del ad_boomerang
				transition_frame_count = TRANSITION_LENGTH*fps
				transition_frames_left = transition_frame_count
				cap.grab() # Flush the buffer
				cap.grab()
				cap.grab()

		if show_ad:
			sleep_dur = ad_last_read+1/fps - time.time()
			if sleep_dur > 0:
				time.sleep(sleep_dur)
			ad_last_read = time.time()
			frame = next(ad_boomerang)
			display_image = frame
			read, ghost_image = cap.read()
			if read:
				display_image = display_image//4*3+ghost_image//4
			cv2.putText(display_image, 'AD', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
			cv2.imshow("frame",display_image)

		if not show_ad:
			_, frame = cap.read()
			#height, width, channels = frame.shape
			ad_frames.append(frame)
			if len(ad_frames)/fps > MAX_AD_LENGTH:
				del ad_frames[0]
			if transition_frames_left > 0:
				frame = frame/transition_frame_count*(transition_frame_count-transition_frames_left)+transition_frame/transition_frame_count*transition_frames_left
				frame = frame.astype('uint8')
				transition_frames_left -= 1
			cv2.imshow("frame",frame)

		sys.stdout.buffer.write(frame.tostring())
		

	cap.release()

if __name__ == "__main__":
	main(sys.argv[1:])

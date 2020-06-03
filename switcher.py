import cv2
import sys
import time

def vcopen(arg):
	cap = cv2.VideoCapture(arg)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
	return cap

MAX_AD_LENGTH = 60 # Seconds
ad_frames = []
ad_idx = 0
ad_dir = 1

def adRead():
	global ad_frames
	global ad_idx
	global ad_dir

	ad_idx += ad_dir
	if ad_idx < 0:
		ad_idx = 0
		ad_dir = 1
	if ad_idx >= len(ad_frames):
		ad_idx = len(ad_frames)-1
		ad_dir = -1
	return ad_frames[ad_idx]

def main(argv):
	global ad_frames
	global ad_idx
	global ad_dir

	cap = vcopen(0)
	cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
	#cap.grab() # Force start the camera
	show_ad = 0
	ad_last_read = 0
	fps = cap.get(cv2.CAP_PROP_FPS)
	while cap.isOpened():

		key = cv2.waitKey(33)
		if key==27:
			print('Switching...', file=sys.stderr)
			if show_ad == 0:
				show_ad = 1
				ad_idx = len(ad_frames)
				ad_dir = -1
			else:
				show_ad = 0
				ad_frames = []
				cap.grab() # Flush the buffer
				cap.grab()
				cap.grab()

		if show_ad:
			sleep_dur = ad_last_read+1/fps - time.time()
			if sleep_dur > 0:
				time.sleep(sleep_dur)
			ad_last_read = time.time()
			frame = adRead()
			_, ghost_image = cap.read()
			display_image = frame//4*3+ghost_image//4
			cv2.putText(display_image, 'AD', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
			cv2.imshow("frame",display_image)

		if not show_ad:
			_, frame = cap.read()
			#height, width, channels = frame.shape
			ad_frames.append(frame)
			if len(ad_frames)/fps > MAX_AD_LENGTH:
				del ad_frames[0]
			cv2.imshow("frame",frame)

		sys.stdout.buffer.write(frame.tostring())
		

	cap.release()

if __name__ == "__main__":
	main(sys.argv[1:])

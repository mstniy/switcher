import cv2
import sys
import time

def vcopen(arg):
	cap = cv2.VideoCapture(arg)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
	return cap

def main(argv):
	adName = argv[0]
	cap_camera = vcopen(0)
	cap_camera.set(cv2.CAP_PROP_BUFFERSIZE, 3)
	cap_camera.grab() # Force start the camera
	cap_ad = vcopen(adName)
	ad_fps = cap_ad.get(cv2.CAP_PROP_FPS)
	ad_last_read = time.time()
	cap = cap_ad
	while cap.isOpened():

		if cap is cap_ad:
			sleep_dur = ad_last_read+1/ad_fps - time.time()
			if sleep_dur > 0:
				time.sleep(sleep_dur)
			ad_last_read = time.time()

		ret, frame = cap.read()
		#height, width, channels = frame.shape
		key = cv2.waitKey(33)
		if key==27:
			print('Switching...', file=sys.stderr)
			if cap is cap_camera:
				cap = cap_ad
			else:
				cap_camera.grab()
				cap_camera.grab()
				cap_camera.grab()
				cap = cap_camera

		if(ret):
			sys.stdout.buffer.write(frame.tostring())
			cv2.imshow("frame",frame)
		else:
			print('Reopening stream...', file=sys.stderr)
			cap.release()
			if cap is cap_camera:
				cap_camera = vcopen(0)
				cap_camera.set(cv2.CAP_PROP_BUFFERSIZE, 3)
				cap_camera.grab() # Force start the camera
				cap = cap_camera
			else:
				cap_ad = vcopen(adName)
				cap = cap_ad

	cap.release()

if __name__ == "__main__":
	main(sys.argv[1:])

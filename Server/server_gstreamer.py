import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib
import cv2
import time

# GStreamer 초기화
Gst.init(None)

# GStreamer 파이프라인 설정
pipeline_str = "udpsrc port=5000 caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264\" ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink"

# GStreamer 파이프라인 실행
pipeline = Gst.parse_launch(pipeline_str)
pipeline.set_state(Gst.State.PLAYING)

cam = cv2.VideoCapture(4)
cam.set(3, 640)
cam.set(4, 480)

frame_count = 0
start_time = time.time()

while True:
	try:
		success, image = cam.read()
		if not success:
			print("Fail to reading webcam")
			continue
		image = cv2.flip(image, 1)
		
		end_time = time.time()
		frame_count += 1
		
		time_interval = end_time - start_time
		
		fps = frame_count / time_interval
		cv2.putText(image, "FPS: {:.2f}".format(fps), (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
		
		frame_count = 0
		start_time = time.time()
		
		cv2.imshow("Rpi4 webcam", image)
		
		if cv2.waitKey(1) == ord('q'):
			print("Quiting rpi4 webcam")
			break
			
		loop = GLib.MainLoop()
		loop.run()
	except KeyboardInterrupt:
		pass

pipeline.set_state(Gst.State.NULL)
cam.release()
cv2.destroyAllWindows()

import numpy as np
import cv2

cap = cv2.VideoCapture('input.h264')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640,480))

while(cap.isOpened()):
	# #print("a")
	# ret = cap.grab()
	# #print("b")
	# ret, frame = cap.retrieve()

	ret, frame = cap.read()
	#print(ret)
	if ret==True:
		# write the frame
		out.write(frame)
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

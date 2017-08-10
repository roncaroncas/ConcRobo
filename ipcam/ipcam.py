import base64
import time
#import urllib2.request

import cv2
import numpy as np


"""
Examples of objects for image frame aquisition from both IP and
physically connected cameras
Requires:
 - opencv (cv2 bindings)
 - numpy
"""


class ipCamera(object):

    def __init__(self, url, user=None, password=None):
        self.url = url
        auth_encoded = base64.encodebytes('%s:%s' % (user, password))[:-1]

        self.req = urllib2.Request(self.url)
        self.req.add_header('Authorization', 'Basic %s' % auth_encoded)

    def isOpened(self):
    	return True


    def get_frame(self):
        response = urllib2.urlopen(self.req)
        img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        return frame


class Camera(object):

    def __init__(self, camera=0):
        self.cam = cv2.VideoCapture(camera)
        if not self.cam:
            raise Exception("Camera not accessible")

        #self.shape = self.get_frame().shape

    def isOpened(self):
    	return self.cam.isOpened()

    def get_frame(self):
        _, frame = self.cam.read()
        return frame

#
#cap = Camera("rtsp://192.168.0.110:34567/user=admin&amp;password=&amp.sdp")
cap = Camera(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while(cap.isOpened()):
    frame = cap.get_frame()
    out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

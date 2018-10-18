import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np

class RaspiCamera:

    def __init__(self, width, height):

        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        #self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.capture_continuous = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

    def capture(self):

        frame = self.capture_continuous.next()
        image = self.rawCapture.array
        self.rawCapture.truncate(0)

        return image

if __name__ == "__main__":

    camera = RaspiCamera(640, 480)
    frame1 = camera.capture()
    frame2 = camera.capture()
    while True:
        
        d=cv2.absdiff(frame1,frame2)
        
        gray=cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(gray,(5,5),0)
        ret,th = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
        dilated = cv2.dilate(th,np.ones((3,3),np.uint8),iterations=3)
        eroded = cv2.erode(dilated,np.ones((3,3),np.uint8),iterations=3)
        c,h=cv2.findContours(eroded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, c, -1, (0, 0, 255), 2)
        
        #cv2.imshow("original",img)
        cv2.imshow("recog",frame1)
        
        frame1=frame2
        frame2 = camera.capture()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cv2.destroyAllWindows()
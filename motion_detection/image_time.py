from datetime import datetime
import picamera
from subprocess import call
from time import sleep


filep="data/"
pictt=3
pics=0
while pics<pictt:
    currt=datetime.now()
    pict=currt.strftime("%Y.%m.%d-%H:%M:%S")
    filen=pict+'.jpg'
    filepp=filep+filen
        
    with picamera.PiCamera() as camera:
        camera.resolution=(1280,720)
        camera.capture(filepp)
        
    print('timestapm')
    timemas=pict
    timecom = "/usr/bin/convert "+filepp+" -pointsize 36 -fill red -annotate +700+650 '"+timemas+"' "+filepp

    call([timecom],shell=True)
    pics += 1
    sleep(5)


    
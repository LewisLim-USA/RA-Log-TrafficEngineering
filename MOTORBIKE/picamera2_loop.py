
from datetime import datetime
from picamera2 import Picamera2, Preview, MappedArray
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder, Quality
import time
import libcamera
import cv2
import platform

#

#create helper function for calculating 10-minute interval
def seconds_till_x_minute(x):
    n = datetime.now()
    v = x * 60 - n.second
    return v


def seconds_till_next_10minute():
    n = datetime.now()
    v = 60*10 - 60*(n.minute % 10) - n.second
    return v

#create helper function to calculate 1-minute interval, used to just test the code/output before launching 10-minute interval runs
def seconds_till_next_minute():
    n = datetime.now()
    return 60-n.second

#record function to handle the recording
def record():
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H_%M_%S")
    fmt = '.mp4'
    root = '/media/steve/BIKE1/data/Mybike1/Video/'
    #'/home/steve/Desktop/Video/'
    width = 320
    height = 240
    camera_name = "Mybike1" #platform.node()
    
    cam = Picamera2()
    preview_config = cam.create_video_configuration(lores={"size":(width,height)},display="lores")
    # Remember to set vflip and hflip for IMX219 8MP Camera.
    # This step is not required for the 16MP AF Camera. 
    #  ,transform=libcamera.Transform(vflip=1,hflip=1)

    colour = (0, 255, 0)
    origin = (0, 30)
    origin_name = (width *2, 30)

    font = cv2.FONT_HERSHEY_DUPLEX
    scale = 0.8
    thickness = 1
        
    def apply_timestamp(request):
      timestamp = time.strftime("%Y-%m-%d %X")
      with MappedArray(request, "main") as m:
          cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
          cv2.putText(m.array, camera_name, origin_name, font, scale, colour, thickness)
   
    cam.configure(preview_config)
    # Afmode: 0=manual, 1=single_autofocus, 2=continuous_autofocus
    cam.set_controls({"AfMode": 2, "AfTrigger": 0}) # continuous_autofocus - may report errors in the status but the picture is still fine
    cam.pre_callback = apply_timestamp
    cam.start()

    time.sleep(2)
    
    while True:
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H_%M_%S")
        output = FfmpegOutput(root + filename + fmt)
        encoder = H264Encoder()
        quality = Quality.VERY_HIGH
        duration = seconds_till_x_minute(2)
        print("duration=" + str(duration) + "seconds, filename=" + filename)
        cam.start_and_record_video(output, encoder, duration = duration, quality = quality)
    
    #cam.stop()
    #cam.stop_preview()

time.sleep(1)
record() 


import cv2
import ipywidgets.widgets as widgets
import threading
import time
import enum
import cv2
#设置摄像头显示组件

image_widget = widgets.Image(format='jpeg', width=500, height=400)
display(image_widget)      #显示摄像头组件

#bgr8转jpeg格式


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])
image = cv2.VideoCapture(0)                           #打开摄像头



# width=1280

# height=960

# cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)#设置图像宽度

# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)#设置图像高度


image.set(3,600)
image.set(4,500)
image.set(5, 30)  #设置帧率
image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
image.set(cv2.CAP_PROP_BRIGHTNESS, 40) #设置亮度 -64 - 64  0.0
image.set(cv2.CAP_PROP_CONTRAST, 50)   #设置对比度 -64 - 64  2.0
image.set(cv2.CAP_PROP_EXPOSURE, 156)  #设置曝光值 1.0 - 5000  156.0

ret, frame = image.read()     #读取摄像头数据
image_widget.value = bgr8_to_jpeg(frame)
while True:
    ret, frame = image.read()
    image_widget.value = bgr8_to_jpeg(frame)
    time.sleep(0.010)

image.release()

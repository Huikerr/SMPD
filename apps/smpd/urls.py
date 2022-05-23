from concurrent.futures import process
from cv2 import CAP_PROP_FPS, VideoWriter
import django
from django.conf import settings
from django.urls import path
from .views import  label,view,video,record
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread, enumerate
from .models import Camera
import os, yaml,time
import cv2 as cv

urlpatterns = [
    path('label/', label),
    path('video/', video),
    path('view/', view),
    path('record/',record)
]

sched = BackgroundScheduler()

sched_stop = False

def detect(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    length, height = gray.shape
    count = 0
    Sum = 0
    for i in range(0, length, 20):
        for j in range(0, height, 20):
            Sum += gray[i,j] / 255
            count += 1
    index = Sum / count
    if index > 0.4 :
        ret = 0
    else:
        ret = -1
    return ret
"""
进行检测
"""
def D_screen(path: str,rtsp: str, name: str):
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, path, 'config.yaml')):
        with open(os.path.join(settings.MEDIA_ROOT, path, 'config.yaml'), 'r') as f:
            content = yaml.load(f.read(), Loader=yaml.FullLoader)
        f.close()
        # cv.namedWindow(name)
        cap = cv.VideoCapture(rtsp)
        out = VideoWriter()
        out.open(os.path.join(settings.MEDIA_ROOT, path, 'out.mp4'),
                 cv.VideoWriter_fourcc(*'mp4v'), cap.get(CAP_PROP_FPS),
                 (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
        count = 0
        while True:
            if sched_stop:
                return 0
            success, frame = cap.read()
            if not success:
                break
            else:
                for i in range(len(content)):
                    startX = int(content[i]['x'])
                    startY = int(content[i]['y'])
                    endX = int(content[i]['x']) + int(content[i]['w'])
                    endY = int(content[i]['y']) + int(content[i]['h'])
                    roi = frame[startY:endY, startX:endX]
                    # print(roi.shape)
                    ret = detect(roi)
                    if ret == 0:
                        msg = "Normal"
                    else:
                        msg = "Black Screen"
                    cv.rectangle(frame,(startX, startY),
                                (endX, endY),
                                (0,0,255),
                                2)
                    cv.putText(frame,msg,(startX, startY),
                                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
                    # 如果有录制一段视频
                    # 并保存
                    if ret == -1:
                        out.write(frame)
                        # print(count)
                        count += 1
                        if count == 3000:
                            # sched.resume_job(job_id='1')
                            # 将摄像头状态关闭
                            camera = Camera.objects.filter(path=path).first()
                            camera.status = False
                            camera.save()
                            out.release()
                            cap.release()
                            return 0
            # cv.imshow(name, frame)
            # key = cv.waitKey(1)
            # if key & 0xff == 27:
            #     break
    else:
        return 0

"""
监测任务
"""
current_thread = []
# 每20分钟监测一次
def monitor():
    print("开启监测任务!")
    print("当前运行线程:", enumerate())
    cameras = Camera.objects.filter(status=True)
    for camera in cameras:
        index = True
        for thread in enumerate():
            if thread.name == "Camera-{}".format(str(camera.id)):
                print("线程{}已在运行中".format(str(camera.id)))
                index = False
            else:
                pass
        if index:
            print("线程Camera-{}开启".format(str(camera.id)))
            thread = Thread(target=D_screen, args=(camera.path, camera.rtsp, camera.name),name="Camera-{}".format(str(camera.id)))
            thread.start()
        else:
            pass

sched.add_job(monitor, 'interval', seconds=60, id='1')
sched.start()
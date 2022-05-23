from django.forms import model_to_dict
from django.shortcuts import render
from .models import Camera
from django.conf import settings
from django.views.decorators import gzip
from django.http.response import StreamingHttpResponse
import json, yaml, cv2, os

# # Create your views here.

"""
标注
"""
def label(request, *args, **kwargs):
    if request.method == 'GET':
        camera = Camera.objects.get(id=request.GET.get('id'))
        dict = model_to_dict(camera)
        dict['picture'] = "http://127.0.0.1:8000/media/" + camera.path + '/label.jpg'
        dict['url'] = "/smpd/label/?id={}".format(str(camera.id))
        return render(request, 'label.html', dict)
    elif request.method == 'POST':
        camera = Camera.objects.get(id=request.POST.get('id'))
        dict = model_to_dict(camera)
        dict['picture'] = "http://127.0.0.1:8000/media/" + camera.path + '/label.jpg'
        dict['url'] = "/smpd/label/?id={}".format(str(camera.id))
        ret = json.loads(request.POST.get('label'))
        with open(os.path.join(settings.MEDIA_ROOT,camera.path,'config.yaml'), 'w') as f:
            f.write(yaml.dump(ret, allow_unicode=True))
        f.close()
        return render(request, 'label.html', dict)
"""
查看摄像头
"""
def view(request, *args, **kwargs):
    data = request.GET.get('id')
    camera = Camera.objects.get(id=data)
    dict = model_to_dict(camera)
    dict["url"] = "http://127.0.0.1:8000/smpd/video/?id={}".format(str(camera.id))
    print(dict["url"])
    return render(request, 'view.html', dict)

"""
查看录制视频
"""
def record(request, *args, **kwargs):
    data = request.GET.get('id')
    camera = Camera.objects.get(id=data)
    dict = model_to_dict(camera)
    dict["url"] = "http://127.0.0.1:8000/media/" + camera.path + "/out.mp4"
    return render(request, 'record.html', dict)

@gzip.gzip_page
def video(request, *args, **kwargs):
    data = request.GET.get('id')
    camera = Camera.objects.get(id=data)
    SHR = StreamingHttpResponse(gen_frames(str(camera.rtsp), str(camera.path)),content_type="multipart/x-mixed-replace;boundary=frame")
    return SHR

def gen_frames(path: str,savepath: str):
    camera = cv2.VideoCapture(path)
    while True:
        success, frame = camera.read()
        # 打开查看就将图片保存进来,直到调整好了，不再看
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, savepath, 'label.jpg'), frame)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

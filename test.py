import cv2 as cv


def D_Monitor(path):
    src = cv.imread(path)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    length, height = gray.shape
    count = 0
    Sum = 0
    for i in range(0, length, 200):
        for j in range(0, height, 200):
            Sum += gray[i,j] / 255
            count += 1
    index = Sum / count
    if index > 0.4 :
        ret = 0
    else:
        ret = -1
    return ret


if __name__ == '__main__':
    # image1 = 'D:\\Huicheng\Desktop\\2022Task\\ITEMS\\SMPD\\images\\1.jpg'
    # image2 = 'D:\\Huicheng\Desktop\\2022Task\\ITEMS\\SMPD\\images\\2.jpg'
    # ret1 = D_Monitor(image1)
    # ret2 = D_Monitor(image2)
    # if ret1 == 0:
    #     print("该屏幕完好!")
    # else:
    #     print("该屏幕黑屏!")
    # if ret2 == 0:
    #         print("该屏幕完好!")
    # else:
    #     print("该屏幕黑屏!")
    # 初始化视频窗口
    windows_name = 'face'
    cv.namedWindow(windows_name)
    video_path = "rtsp://admin:a123123123@192.168.1.64:554/h264/ch1/main/av_stream"
    cap = cv.VideoCapture("rtsp://admin:a123123123@192.168.1.64:554/h264/ch1/main/av_stream")
    while True:
        # 从摄像头读取一帧图像
        success, image = cap.read()
        if not success:
            break
        cv.imshow(windows_name, image)
        key = cv.waitKey(1)
        if key & 0xff == 27:
            break

    # 释放设备资源，销毁窗口
    cap.release()
    cv.destroyAllWindows()



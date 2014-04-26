import picamera
import threading

class CamThread(threading.Thread):
    def __init__(self):
        super(CamThread,self).__init__()
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024,768)

    def run(self):
        self.camera.capture('mugshot.jpg')
        print("captured")
        self.camera.close()


if __name__ == '__main__':
    cam_thread=CamThread()
    print("start")
    cam_thread.start()
    print("waiting for thread")
    cam_thread.join()
    print("done")

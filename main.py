from vehicle_counter.detector.real_time_detector import RealTimeDetector
from vehicle_counter.detector.static_detector import StaticDetector
from vehicle_counter.model.camera import Camera


def real_time(source):
    camera = Camera.objects(name='real time test').first()
    if not camera:
        camera = Camera(name='real time test', location='AP-7')
        camera.save()
    detector = RealTimeDetector(source, camera)
    detector.continuous_detection(show_detections=True)


def from_static_image(source):
    camera = Camera.objects(name='static test').first()
    if not camera:
        camera = Camera(name='static test', location='Rambla de Girona')
        camera.save()

    detector = StaticDetector(source, camera)
    detector.show_detections()


if __name__ == '__main__':
    from mongoengine import connect
    connect(host="mongodb://127.0.0.1:27017/vehicle_counter")

    #real_time('/home/u1920603/PycharmProjects/vehicle_counter/tests/video.mp4')
    from_static_image('/home/u1920603/Descargas/recorder/pics/inventory/5.jpg')

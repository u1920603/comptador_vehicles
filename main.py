from vehicle_counter.detector.real_time_detector import RealTimeDetector
from vehicle_counter.detector.static_detector import StaticDetector
from vehicle_counter.model.camera import Camera


def real_time(source, name, location):
    camera = Camera.objects(name=name).first()
    if not camera:
        camera = Camera(name=name, location=location)
        camera.save()
    detector = RealTimeDetector(source, camera)
    detector.continuous_detection(show_detections=True)


def from_static_image(source, name, location):
    camera = Camera.objects(name=name).first()
    if not camera:
        camera = Camera(name=name, location=location)
        camera.save()

    detector = StaticDetector(source, camera)
    detector.show_detections()


if __name__ == '__main__':
    from mongoengine import connect
    connect(host="mongodb://mongodb:27017/vehicle_counter")

    #real_time('/code/tests/video.mp4', 'real time test', 'AP-7')
    from_static_image('/code/tests/3.jpg', 'static test', 'Rambla de Girona')

"""Real time detector."""
import time
from datetime import datetime

import cv2

from vehicle_counter.detector.detector import Detector
from vehicle_counter.image_modifier.image_modifier import ImageModifier, MiddleLine
from vehicle_counter.model.camera import Camera
from vehicle_counter.model.history_registry import HistoryRegistry, Direction


class RealTimeDetector(Detector):
    """Real time detector implementation."""
    def __init__(self, source, camera: Camera = None) -> None:
        """Constructor."""
        self.cap = cv2.VideoCapture(source)

        self.upload_to_database_time = 30
        self.uploaded_at = time.time()

        success, img = self.cap.read()
        super().__init__(img, camera)

    def upload_to_database(self):
        """Upload result to database."""
        history_registry = HistoryRegistry(timestamp=datetime.utcnow(), co2_impact=self.total_carbon_footprint)
        history_registry.up = Direction(
            total_cars=self.counter.up_list[0],
            total_motorbikes=self.counter.up_list[1],
            total_buses=self.counter.up_list[2],
            total_trucks=self.counter.up_list[3]
        )
        history_registry.down = Direction(
            total_cars=self.counter.down_list[0],
            total_motorbikes=self.counter.down_list[1],
            total_buses=self.counter.down_list[2],
            total_trucks=self.counter.down_list[3]
        )
        history_registry.total_cars = self.counter.up_list[0] + self.counter.down_list[0]
        history_registry.total_motorbikes = self.counter.up_list[1] + self.counter.down_list[1]
        history_registry.total_buses = self.counter.up_list[2] + self.counter.down_list[2]
        history_registry.total_trucks = self.counter.up_list[3] + self.counter.down_list[3]

        if self.camera:
            self.camera.measurements.append(history_registry)
            self.camera.updated_at = datetime.utcnow()
            self.camera.save()

    def update_source(self, img) -> None:
        """Update detector source."""
        input_size = 320

        self.img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        blob = cv2.dnn.blobFromImage(self.img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)
        self.network.setInput(blob)
        self.frequencies()

        if (time.time() - self.uploaded_at) > self.upload_to_database_time:
            self.uploaded_at = time.time()
            self.upload_to_database()

    def continuous_detection(self, show_detections=True):
        """Continuously detection."""
        while self.cap.isOpened():
            success, img = self.cap.read()
            if img is not None:
                self.update_source(img)
                if show_detections:
                    image_modifier = ImageModifier(self.img)
                    image_modifier.draw_middle_line(MiddleLine())
                    image_modifier.draw_carbon_footprint(self.total_carbon_footprint)
                    image_modifier.draw_lane_resume(self.counter.up_list, self.counter.down_list)
                    image_modifier.show_image()
            else:
                break
            if cv2.waitKey(1) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

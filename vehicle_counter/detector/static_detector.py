"""Static detector."""

import cv2
from datetime import datetime
from vehicle_counter.carbon_estimator.simple_carbon_estimator import CarbonEstimator
from vehicle_counter.detector.detector import Detector
from vehicle_counter.image_modifier.image_modifier import ImageModifier
from vehicle_counter.model.camera import Camera
from vehicle_counter.model.history_registry import HistoryRegistry


class StaticDetector(Detector):
    """Static detector implementation."""
    def __init__(self, source: str, camera: Camera = None) -> None:
        img = cv2.imread(source)
        super().__init__(img, camera)

        self.freq = {}

    def upload_to_database(self) -> None:
        """Upload detections to database."""
        history_registry = HistoryRegistry(timestamp=datetime.utcnow(), co2_impact=self.total_carbon_footprint)
        for key, value in self.freq.items():
            if key == 'car':
                history_registry.total_cars = value
            elif key == 'bus':
                history_registry.total_buses = value
            elif key == 'truck':
                history_registry.total_trucks = value
            elif key == 'motorbike':
                history_registry.total_motorbikes = value
        if self.camera:
            self.camera.measurements.append(history_registry)
            self.camera.updated_at = datetime.utcnow()
            self.camera.save()

    def show_detections(self):
        """Show detection in a new window."""
        self.freq = self.frequencies()

        for key, value in self.freq.items():
            self.total_carbon_footprint = self.total_carbon_footprint + CarbonEstimator(key).get_estimation() * value

        self.upload_to_database()

        modified_image = ImageModifier(self.img)
        modified_image.draw_carbon_footprint(self.total_carbon_footprint)
        modified_image.draw_simple_resume(self.freq)
        modified_image.show_image(wait=True)

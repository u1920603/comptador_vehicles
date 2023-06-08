"""Detector."""

import collections

import cv2
import numpy as np

from config import CONFIG
from vehicle_counter.carbon_estimator.simple_carbon_estimator import CarbonEstimator
from vehicle_counter.counter.counter import VehicleCounter
from vehicle_counter.detector.coco_names import CocoNames

from vehicle_counter.image_modifier.image_modifier import ImageModifier
from vehicle_counter.model.camera import Camera
from vehicle_counter.tracker.euclidean_tracker import EuclideanDistanceTracker


class Detector:
    """Basic detector implementation."""

    def __init__(self, img, camera: Camera = None) -> None:
        CONFIG.load()
        self.detection_threshold = CONFIG.detection.threshold
        self.nms_threshold = CONFIG.detection.nms_threshold
        self.coco_names = CocoNames(CONFIG.coco.file)

        input_size = 320
        self.img = img
        self.network = cv2.dnn.readNetFromDarknet(CONFIG.model.model_configuration, CONFIG.model.model_weights)
        blob = cv2.dnn.blobFromImage(self.img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)
        self.network.setInput(blob)

        self.tracker = EuclideanDistanceTracker()
        self.counter = VehicleCounter()

        self.total_carbon_footprint = 0

        self.camera = camera

    def enable_gpu_acceleration(self):
        """Enable GPU acceleration."""
        self.network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def get_detection(self) -> list:
        """Return a list of detections."""
        layers_names = self.network.getLayerNames()
        output_names = [(layers_names[i[0] - 1]) for i in self.network.getUnconnectedOutLayers()]
        outputs = self.network.forward(output_names)
        return outputs

    def frequencies(self) -> dict:
        """Return dictionary with frequencies detections by class name."""
        outputs = self.get_detection()
        vehicles_detections = self.post_process(outputs)
        frequencies = collections.Counter(vehicles_detections)
        return frequencies

    @staticmethod
    def non_max_suppression(boxes, confidence_scores, conf_threshold, nms_threshold):
        """Apply non max suppression."""
        indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, conf_threshold, nms_threshold)
        return indices

    def post_process(self, outputs) -> list:
        """Return a list of detections totals."""
        boxes, class_ids, confidence_scores = self.generate_outputs(outputs)
        detected_class_names = self.generate_detections(boxes, class_ids, confidence_scores)
        return detected_class_names

    def generate_outputs(self, outputs):
        """Generate detection raw output."""
        boxes = []
        class_ids = []
        confidence_scores = []

        height, width = self.img.shape[:2]

        for output in outputs:
            for det in output:
                scores = det[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if self.coco_names.is_useful_object(class_id):
                    if confidence > self.detection_threshold:
                        w, h = int(det[2] * width), int(det[3] * height)
                        x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)
                        boxes.append([x, y, w, h])
                        class_ids.append(class_id)
                        confidence_scores.append(float(confidence))

        return boxes, class_ids, confidence_scores

    def generate_detections(self, boxes, class_ids, confidence_scores) -> list:
        """Return a list of detections."""
        detected_class_names = []
        detection = []
        indices = self.non_max_suppression(boxes, confidence_scores, self.detection_threshold, self.nms_threshold)
        if indices is not None and len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]

                vehicle_type = self.coco_names.name(class_ids[i])
                detected_class_names.append(vehicle_type)

                carbon_food_print_estimation = CarbonEstimator(vehicle_type).get_estimation()

                color = [int(c) for c in self.coco_names.color(class_ids[i])]
                image_modifier = ImageModifier(self.img)
                image_modifier.draw_rectangle_header(vehicle_type, color, x, y, confidence_scores[i],
                                                     carbon_food_print_estimation)
                image_modifier.draw_detection_rectangle(x, y, w, h, color)

                detection.append([x, y, w, h, self.coco_names.required_class_index.index(class_ids[i])])

            boxes_ids = self.tracker.update(detection)
            for box_id in boxes_ids:
                self.counter.count(box_id, self.img)

            self.calculate_carbon_footprint()

        return detected_class_names

    def calculate_carbon_footprint(self):
        cars = CarbonEstimator(self.coco_names.name_from_selected(0)).get_estimation()
        motorbike = CarbonEstimator(self.coco_names.name_from_selected(1)).get_estimation()
        bus = CarbonEstimator(self.coco_names.name_from_selected(2)).get_estimation()
        truck = CarbonEstimator(self.coco_names.name_from_selected(3)).get_estimation()

        carbon_footprint_up = self.counter.up_list[0] * cars + self.counter.up_list[1] * motorbike + \
                              self.counter.up_list[2] * bus + self.counter.up_list[3] * truck
        carbon_footprint_down = self.counter.down_list[0] * cars + self.counter.down_list[1] * motorbike + \
                                self.counter.down_list[2] * bus + self.counter.down_list[3] * truck

        self.total_carbon_footprint = carbon_footprint_up + carbon_footprint_down

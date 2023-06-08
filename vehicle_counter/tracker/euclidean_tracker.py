"""Euclidean distance tracker."""


import math
from vehicle_counter.tracker.tracker import Tracker


class EuclideanDistanceTracker(Tracker):
    """Implementation of Euclidean distance tracker."""
    def __init__(self) -> None:
        self.center_points = {}
        self.id_count = 0

    def update(self, detections) -> list:
        """Update tracker."""
        objects_bbs_ids = self.add_new_objects_ids(detections)
        self.clen_not_used_ids(objects_bbs_ids)
        return objects_bbs_ids

    def clen_not_used_ids(self, objects_bbs_ids: list) -> None:
        """Clear old ids."""
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, index = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
        self.center_points = new_center_points.copy()

    def add_new_objects_ids(self, objects_rect) -> list:
        """Add new objects to track."""
        objects_bbs_ids = []
        for rect in objects_rect:
            same_object_detected = self.is_new_object_id(objects_bbs_ids, rect)
            if not same_object_detected:
                self.add_new_object_id(objects_bbs_ids, rect)

        return objects_bbs_ids

    def add_new_object_id(self, objects_bbs_ids: list, rect) -> list:
        """Add new object to counter."""
        x, y, w, h, index = rect
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        self.center_points[self.id_count] = (cx, cy)
        objects_bbs_ids.append([x, y, w, h, self.id_count, index])
        self.id_count += 1

        return objects_bbs_ids

    def is_new_object_id(self, objects_bbs_ids: list, rect) -> bool:
        """Return true is object has been already tracked. False otherwise."""
        x, y, w, h, index = rect
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        new_object = False
        for object_id, pt in self.center_points.items():
            dist = math.hypot(cx - pt[0], cy - pt[1])
            if dist < 25:
                self.center_points[object_id] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, object_id, index])
                new_object = True
                return new_object
        return new_object

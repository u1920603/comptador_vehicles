"""Vehicle counter."""

import cv2
from vehicle_counter.detector.middle_line import MiddleLine


class VehicleCounter:
    """Vehicle counter."""

    def __init__(self):
        self.temp_up_list = []
        self.temp_down_list = []
        self.up_list = [0, 0, 0, 0]
        self.down_list = [0, 0, 0, 0]

        self.middle_line = MiddleLine()

    def count(self, box_id, img):
        """Count vehicles in img."""
        x, y, width, height, id, index = box_id

        center = self.find_center(x, y, width, height)
        ix, iy = center

        if (iy > self.middle_line.up_line_position) and (iy < self.middle_line.middle_line_position):

            if id not in self.temp_up_list:
                self.temp_up_list.append(id)

        elif self.middle_line.down_line_position > iy > self.middle_line.middle_line_position:
            if id not in self.temp_down_list:
                self.temp_down_list.append(id)

        elif iy < self.middle_line.up_line_position:
            if id in self.temp_down_list:
                self.temp_down_list.remove(id)
                self.up_list[index] = self.up_list[index] + 1

        elif iy > self.middle_line.down_line_position:
            if id in self.temp_up_list:
                self.temp_up_list.remove(id)
                self.down_list[index] = self.down_list[index] + 1

        self.draw_middle_point(img, center)

    @staticmethod
    def draw_middle_point(img, center) -> None:
        """Draw middle point."""
        cv2.circle(img, center, 2, (0, 0, 255), -1)

    @staticmethod
    def find_center(x, y, width, height):
        """Find center of the object."""
        x1 = int(width / 2)
        y1 = int(height / 2)
        cx = x + x1
        cy = y + y1
        return cx, cy

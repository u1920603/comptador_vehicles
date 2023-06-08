"""Image modifier"""

import cv2

from vehicle_counter.detector.middle_line import MiddleLine


class ImageModifier:

    def __init__(self, img) -> None:
        self.img = img

    def show_image(self, wait=False) -> None:
        """Show image in the screen."""
        cv2.imshow("image", self.img)
        if wait:
            cv2.waitKey(0)

    def draw_rectangle_header(self, name, color, x, y, score, carbon_food_print_estimation) -> None:
        """Show information to a specified points of origen."""
        # Vehicle type
        self.draw_name(name, color, x, y, score)

        # C02 info
        self.draw_carbon_estimation(color, x, y, carbon_food_print_estimation)

    def draw_name(self, name, color, x, y, score) -> None:
        """Show name to specified points."""
        cv2.putText(
            self.img,
            f'{name.upper()} {int(score * 100)}%',
            (x, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1
        )

    def draw_carbon_estimation(self, color, x, y, carbon_food_print_estimation) -> None:
        """Show carbon estimation."""
        cv2.putText(
            self.img,
            f'CO2: {carbon_food_print_estimation} g',
            (x, y - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            color,
            1
        )

    def draw_detection_rectangle(self, x, y, w, h, color) -> None:
        """Show rectangle in a specific coordinates."""
        cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)

    def draw_simple_resume(self, frequencies) -> None:
        """Show simple resume."""
        text_color = [225, 255, 255]
        text_font_face = 0
        text_font_sale = 0.5
        text_thickness = 1

        line_color = [85, 45, 255]
        line_thickness = 20

        for idx, (key, value) in enumerate(frequencies.items()):
            display_text = f"{key.capitalize() if value< 1 else key.capitalize() + 's'}: {value}"
            cv2.line(
                self.img,
                (20, 40 + (idx*30)),
                (len(display_text*10), 40 + (idx*30)),
                line_color,
                line_thickness
            )
            cv2.putText(
                self.img,
                display_text,
                (10, 45 + (idx*30)),
                text_font_face,
                text_font_sale,
                text_color,
                thickness=text_thickness,
                lineType=cv2.LINE_AA
            )

    def draw_middle_line(self, middle_line: MiddleLine) -> None:
        """Show middle line."""
        ih, iw, channels = self.img.shape
        cv2.line(self.img, (0, middle_line.up_line_position), (iw, middle_line.up_line_position), (0, 0, 255), 2)
        cv2.line(self.img, (0, middle_line.middle_line_position), (iw, middle_line.middle_line_position), (0, 255, 0), 2)
        cv2.line(self.img, (0, middle_line.down_line_position), (iw, middle_line.down_line_position), (0, 0, 255), 2)

    def draw_lane_resume(self, up_list, down_list) -> None:
        """Show lane resume."""
        if down_list[0] > 0 or up_list[0] or down_list[1] > 0 or up_list[1] > 0 or down_list[2] > 0 or up_list[2] > 0 or down_list[3] > 0 or up_list[3] > 0:
            cv2.line(self.img, (110, 35), (205, 35), [85, 45, 255], 20)
            cv2.putText(self.img, f'Down', (110, 40), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'Up', (170, 40), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        if down_list[0] > 0 or up_list[0] > 0:
            cv2.line(self.img, (10, 60), (205, 60), [85, 45, 255], 20)
            cv2.putText(self.img, f'Cars:', (10, 65), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{down_list[0]}', (110, 65), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{up_list[0]}', (170, 65), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        if down_list[1] > 0 or up_list[1] > 0:
            cv2.line(self.img, (10, 85), (205, 85), [85, 45, 255], 20)
            cv2.putText(self.img, f'Motorbike:', (10, 90), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{down_list[2]}', (110, 90), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{up_list[2]}', (170, 90), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        if down_list[2] > 0 or up_list[2] > 0:
            cv2.line(self.img, (10, 110), (205, 110), [85, 45, 255], 20)
            cv2.putText(self.img, f'Bus:', (10, 115), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{down_list[2]}', (110, 115), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{up_list[2]}', (170, 115), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        if down_list[3] > 0 or up_list[3] > 0:
            cv2.line(self.img, (10, 135), (205, 135), [85, 45, 255], 20)
            cv2.putText(self.img, f'Truck:', (10, 130), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{down_list[3]}', (110, 130), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(self.img, f'{up_list[3]}', (170, 130), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    def draw_carbon_footprint(self, total_carbon_footprint) -> None:
        """Show carbon footprint."""
        cv2.line(self.img, (20, 10), (150, 10), [85, 45, 255], 20)
        cv2.putText(self.img, f'C02:', (15, 14), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(self.img, f'{total_carbon_footprint}g', (60, 14), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)

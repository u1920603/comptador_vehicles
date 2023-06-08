"""Middle line."""


class MiddleLine:
    """Middle line definition."""
    def __init__(self, middle_line_position=255):
        self.middle_line_position = middle_line_position
        self.up_line_position = middle_line_position - 15
        self.down_line_position = middle_line_position + 15

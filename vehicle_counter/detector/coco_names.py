"""Coco names mappings."""

import numpy as np


class CocoNames:

    def __init__(self, file_path):
        self.class_names = open(file_path).read().strip().split('\n')
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.class_names), 3), dtype='uint8')
        self.required_class_index = [2, 3, 5, 7]

    def color(self, index) -> list:
        """Return color for coco index."""
        return self.colors[index]

    def name(self, index) -> str:
        """Return index for coco name."""
        return self.class_names[index]

    def is_useful_object(self, object_id) -> bool:
        """Return true if coco index is used, false otherwise."""
        return object_id in self.required_class_index

    def name_from_selected(self, index) -> str:
        """Return coco name from selected indexes."""
        return self.class_names[self.required_class_index[index]]

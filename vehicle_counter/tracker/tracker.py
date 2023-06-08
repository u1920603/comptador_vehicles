"""Tracker."""

from abc import ABC, abstractmethod


class Tracker(ABC):
    """Tracker definition."""

    @abstractmethod
    def update(self, detections) -> list:
        """Update tracker."""
        ...

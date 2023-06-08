"""Carbon footprint estimator generic class."""

from abc import abstractmethod


class Estimator:
    """Carbon footprint estimator."""

    @abstractmethod
    def get_estimation(self) -> float:
        """Return carbon foot print estimation."""
        ...

"""Simple carbon footprint estimator."""

from vehicle_counter.carbon_estimator.estimator import Estimator


class CarbonEstimator(Estimator):
    """Simple co2 estimator."""

    def __init__(self, vehicle_type, distance_travelled=1) -> None:
        self.vehicle_type = vehicle_type
        self.distance_travelled = distance_travelled

    @staticmethod
    def carbon_footprint_type(vehicle_type: str) -> float:
        """Return vehicle type carbon footprint per 1 km."""
        # OpenTripPlanner project
        # g per 1KM
        carbon_footprint = {
            'bicycle': 0,
            'car': 220,
            'bus': 863,
            'truck': 920,
            'motorbike': 79
        }

        return carbon_footprint.get(vehicle_type, 0)

    def get_estimation(self) -> float:
        """Return carbon foot print estimation."""
        return self.carbon_footprint_type(self.vehicle_type) * self.distance_travelled

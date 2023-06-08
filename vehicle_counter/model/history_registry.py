"""History registry model definition."""

from datetime import datetime

from mongoengine import IntField, DateTimeField, EmbeddedDocument, FloatField, EmbeddedDocumentField


class Direction(EmbeddedDocument):
    """Register vehicle count for direction."""
    total_cars = IntField(default=0)
    total_buses = IntField(default=0)
    total_trucks = IntField(default=0)
    total_motorbikes = IntField(default=0)


class HistoryRegistry(EmbeddedDocument):
    """Register vehicles counts at specific time."""
    total_cars = IntField(default=0)
    total_buses = IntField(default=0)
    total_trucks = IntField(default=0)
    total_motorbikes = IntField(default=0)
    co2_impact = FloatField(default=0)

    up = EmbeddedDocumentField(Direction)
    down = EmbeddedDocumentField(Direction)

    timestamp = DateTimeField(default=datetime.utcnow)

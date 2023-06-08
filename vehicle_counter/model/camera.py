"""Camera model object definition."""

from datetime import datetime
from mongoengine import Document, DateTimeField, ListField, EmbeddedDocumentField, StringField

from vehicle_counter.model.history_registry import HistoryRegistry


class Camera(Document):
    """Camera type."""
    name = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=None)
    location = StringField()

    measurements = ListField(EmbeddedDocumentField(HistoryRegistry))

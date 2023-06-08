from dataclasses import dataclass, field
from pathlib import Path

from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass()
class CocoConfig(DataClassJsonMixin):
    file: str


@dataclass
class ModelConfig(DataClassJsonMixin):
    model_configuration: str
    model_weights: str


@dataclass
class DetectionConfig(DataClassJsonMixin):
    threshold: float
    nms_threshold: float


@dataclass
class Config(YamlDataClassConfig):
    model: ModelConfig = field(
        default=None,
        metadata={'dataclasses_json': {'model': ModelConfig}}
    )
    detection: DetectionConfig = field(
        default=None,
        metadata={'dataclasses_json': {'detection': DetectionConfig}}
    )

    coco: CocoConfig = field(
        default=None,
        metadata={'dataclasses_json': {'file': CocoConfig}}
    )

    FILE_PATH: Path = create_file_path_field(Path(__file__).parent.parent / 'config/config.yaml')


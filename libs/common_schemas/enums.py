from enum import Enum

class ViolationType(str, Enum):
    SPEEDING = "SPEEDING"
    RED_LIGHT = "RED_LIGHT"
    WRONG_WAY = "WRONG_WAY"
    ILLEGAL_PARKING = "ILLEGAL_PARKING"
    NO_HELMET = "NO_HELMET"
    STOP_LINE = "STOP_LINE"
    NO_SEATBELT = "NO_SEATBELT"
    TRIPLE_RIDING = "TRIPLE_RIDING"

class CameraStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"
    ERROR = "ERROR"

class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class AssetType(str, Enum):
    CAMERA = "CAMERA"
    RADAR = "RADAR"
    LIDAR = "LIDAR"
    SENSOR = "SENSOR"

class QueueTopic(str, Enum):
    INGESTION = "INGESTION"
    DETECTIONS = "DETECTIONS"
    TRACKS = "TRACKS"
    VIOLATIONS = "VIOLATIONS"
    INCIDENTS = "INCIDENTS"

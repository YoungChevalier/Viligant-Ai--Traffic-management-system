import json
import logging
from typing import Dict, Any

from libs.queue_contracts.topics import RAW_FRAME_TOPIC
from libs.queue_contracts.envelope import build_queue_envelope

logger = logging.getLogger(__name__)


def publish_raw_frame_job(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Wraps the given payload in a QueueEnvelope and publishes it
    to the raw-frame topic.

    In production this would push to Redis Streams / Kafka / RabbitMQ.
    Currently logs the envelope for local development.

    Returns the serialised envelope dict.
    """
    envelope = build_queue_envelope(payload=payload, topic=RAW_FRAME_TOPIC)
    envelope_dict = envelope.model_dump(mode="json")

    # TODO: replace with actual queue client call
    logger.info("Publishing to %s: %s", RAW_FRAME_TOPIC, json.dumps(envelope_dict))

    return envelope_dict

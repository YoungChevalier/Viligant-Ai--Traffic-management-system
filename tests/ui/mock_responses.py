"""
mock_responses.py
Pre-canned API response data for Playwright UI tests.
All tests intercept network requests and return this data,
so we never depend on a live backend.
"""

MOCK_INCIDENTS_LIST = {
    "total": 5,
    "limit": 10,
    "offset": 0,
    "incidents": [
        {
            "incident_id": "INC-2026-00001",
            "timestamp": "2026-06-18T10:30:00Z",
            "created_at": "2026-06-18T10:30:00Z",
            "camera_id": "cam-northex-01",
            "primary_violation": "NO_HELMET",
            "status": "OPEN",
            "zone": "North",
            "violations": [{
                "violation_type": "NO_HELMET",
                "confidence": 0.92,
                "plate_text": "MH12AB1234",
                "plate_confidence": 0.88
            }],
            "evidence_assets": [],
            "reviews": []
        },
        {
            "incident_id": "INC-2026-00002",
            "timestamp": "2026-06-17T14:15:00Z",
            "created_at": "2026-06-17T14:15:00Z",
            "camera_id": "cam-southex-02",
            "primary_violation": "TRIPLE_RIDING",
            "status": "APPROVED",
            "zone": "South",
            "violations": [{
                "violation_type": "TRIPLE_RIDING",
                "confidence": 0.85,
                "plate_text": "DL4CAF5678",
                "plate_confidence": 0.91
            }],
            "evidence_assets": [],
            "reviews": [{
                "reviewer_id": "rev_admin_02",
                "action": "APPROVE",
                "notes": "Clear violation confirmed.",
                "created_at": "2026-06-17T15:00:00Z"
            }]
        },
        {
            "incident_id": "INC-2026-00003",
            "timestamp": "2026-06-16T08:45:00Z",
            "created_at": "2026-06-16T08:45:00Z",
            "camera_id": "cam-east-03",
            "primary_violation": "NO_HELMET",
            "status": "REJECTED",
            "zone": "East",
            "violations": [{
                "violation_type": "NO_HELMET",
                "confidence": 0.67,
                "plate_text": "KA01MG9012",
                "plate_confidence": 0.79
            }],
            "evidence_assets": [],
            "reviews": [{
                "reviewer_id": "rev_operator_01",
                "action": "REJECT",
                "notes": "False positive - wearing a cap, not bare head.",
                "created_at": "2026-06-16T09:30:00Z"
            }]
        },
        {
            "incident_id": "INC-2026-00004",
            "timestamp": "2026-06-15T19:00:00Z",
            "created_at": "2026-06-15T19:00:00Z",
            "camera_id": "cam-west-04",
            "primary_violation": "NO_HELMET",
            "status": "ESCALATED",
            "zone": "West",
            "violations": [{
                "violation_type": "NO_HELMET",
                "confidence": 0.55,
                "plate_text": None,
                "plate_confidence": None
            }],
            "evidence_assets": [],
            "reviews": [{
                "reviewer_id": "rev_operator_01",
                "action": "ESCALATE",
                "notes": "Image too dark, needs admin.",
                "created_at": "2026-06-15T20:00:00Z"
            }]
        },
        {
            "incident_id": "INC-2026-00005",
            "timestamp": "2026-06-14T11:20:00Z",
            "created_at": "2026-06-14T11:20:00Z",
            "camera_id": "cam-central-05",
            "primary_violation": "TRIPLE_RIDING",
            "status": "OPEN",
            "zone": "Central",
            "violations": [{
                "violation_type": "TRIPLE_RIDING",
                "confidence": 0.78,
                "plate_text": "RJ14EF7890",
                "plate_confidence": 0.84
            }],
            "evidence_assets": [],
            "reviews": []
        }
    ]
}

MOCK_STATS = {
    "total": 5,
    "by_status": {
        "OPEN": 2,
        "APPROVED": 1,
        "REJECTED": 1,
        "ESCALATED": 1
    },
    "by_violation_type": {
        "NO_HELMET": 3,
        "TRIPLE_RIDING": 2
    },
    "by_camera": {
        "cam-northex-01": 1,
        "cam-southex-02": 1,
        "cam-east-03": 1,
        "cam-west-04": 1,
        "cam-central-05": 1
    },
    "by_day": {
        "2026-06-14": 1,
        "2026-06-15": 1,
        "2026-06-16": 1,
        "2026-06-17": 1,
        "2026-06-18": 1
    }
}

MOCK_INCIDENT_DETAIL = MOCK_INCIDENTS_LIST["incidents"][0]

MOCK_REVIEW_RESPONSE = {
    "status": "success",
    "data": {
        "incident_id": "INC-2026-00001",
        "action": "REJECT",
        "new_status": "REJECTED",
        "queue_status": "none"
    }
}

# Filtered result: only OPEN incidents
MOCK_INCIDENTS_OPEN_ONLY = {
    "total": 2,
    "limit": 10,
    "offset": 0,
    "incidents": [inc for inc in MOCK_INCIDENTS_LIST["incidents"] if inc["status"] == "OPEN"]
}

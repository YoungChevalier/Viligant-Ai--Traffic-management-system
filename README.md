# Traffic Violation Management System

An automated, microservice-based pipeline for identifying and classifying traffic violations (e.g., No Helmet) using Computer Vision and License Plate Recognition (ANPR).

## System Architecture

The system follows an event-driven vertical slice architecture. Cameras push frames to the Ingestion layer, which cascades through CV processing, Business Rules, and Evidence Fusion before landing in a Human Review Queue.

```mermaid
flowchart TD
    Cam[Edge Camera] -->|HTTP POST| Ing[Ingestion Service]
    Ing -->|Queue| Prep[Preprocessing]
    Prep -->|Queue| Det[Detection (YOLO)]
    Det -->|Queue| Trk[Tracking (DeepSORT)]
    Trk -->|Queue| Rule[Helmet Rule Engine]
    
    Rule -->|Compliant| Drop((Drop))
    Rule -->|Violation| ANPR[ANPR Service]
    
    ANPR -->|Queue| Evid[Evidence & Fusion]
    Evid -->|DB Insert| Dash[Dashboard & Review API]
    Dash --- UI[Frontend UI]
    
    Dash -->|Decisions| Ana[Analytics Store]
    Dash -->|Hard Examples| ML[Model Lifecycle Intake]
```

## Quick Links
- [Developer & Setup Guide](docs/DEVELOPER_GUIDE.md)
- [API Overview](docs/API_OVERVIEW.md)
- [Operational Runbook](docs/OPERATIONAL_RUNBOOK.md)

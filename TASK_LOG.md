# Task Log

> Tracks every task executed against this repository. No task should be merged without an entry here.

| task_id | description | files_changed | status | notes |
|---------|-------------|---------------|--------|-------|
| 0.1.1 | Create service folder structure | `services/*/app/__init__.py`, `services/*/tests/__init__.py` | ✅ Done | Scaffold only, no logic |
| 0.1.2 | Create internal app structure per service | `services/*/app/api/`, `services/*/app/services/` | ✅ Done | Empty packages |
| 0.2.1 | Create shared enum file | `libs/common-schemas/enums.py` | ✅ Done | No pydantic bodies |
| 0.2.2 | Create frame schema | `libs/common-schemas/frame.py` | ✅ Done | |
| 0.2.3 | Create detection schema | `libs/common-schemas/detection.py` | ✅ Done | |
| 0.2.4 | Create tracking schema | `libs/common-schemas/tracking.py` | ✅ Done | |
| 0.2.5 | Create ANPR schema | `libs/common-schemas/anpr.py` | ✅ Done | |
| 0.2.6 | Create incident schema | `libs/common-schemas/incident.py` | ✅ Done | |
| 0.2.7 | Create evidence schema | `libs/common-schemas/evidence.py` | ✅ Done | |
| 0.2.8 | Create review schema | `libs/common-schemas/review.py` | ✅ Done | |
| 0.3.1 | Create queue topic constants | `libs/queue-contracts/topics.py` | ✅ Done | |
| 0.3.2 | Create queue envelope schema | `libs/queue-contracts/envelope.py` | ✅ Done | No Redis/Kafka client |
| 0.4.1 | Create time helpers | `libs/common-utils/time_utils.py` | ✅ Done | |
| 0.4.2 | Create ID helpers | `libs/common-utils/id_utils.py` | ✅ Done | |
| 0.4.3 | Create file-path helpers | `libs/common-utils/path_utils.py` | ✅ Done | |
| 0.5.1 | Create DB naming convention | `libs/common-utils/db_naming.py` | ✅ Done | Deterministic constraint names |
| 0.6.1 | Create DB Base config | `services/persistence/app/db/base.py` | ✅ Done | |
| 0.6.2 | Create DB session setup | `services/persistence/app/db/session.py` | ✅ Done | No models here |
| 0.6.3 | Create camera models | `services/persistence/app/models/camera_models.py` | ✅ Done | Camera, CameraCalibration, CameraZone |
| 0.6.4 | Create frame models | `services/persistence/app/models/frame_models.py` | ✅ Done | Frame, FrameQualityMetric |
| 0.6.5 | Create detection models | `services/persistence/app/models/detection_models.py` | ✅ Done | Detection |
| 0.6.6 | Create tracking models | `services/persistence/app/models/tracking_models.py` | ✅ Done | Track, TrackHistory |
| 0.6.7 | Create ANPR models | `services/persistence/app/models/anpr_models.py` | ✅ Done | PlateRead, PlateCandidateRecord |
| 0.6.8 | Create incident models | `services/persistence/app/models/incident_models.py` | ✅ Done | ViolationCandidateRecord, Incident, IncidentScore, EvidenceAsset, ReviewAction |
| 0.7.1 | Initialize Alembic | `services/persistence/alembic.ini`, `services/persistence/alembic/env.py` | ✅ Done | Imports all models for autogenerate |
| 0.7.2 | Migration: camera tables | `services/persistence/alembic/versions/0001_create_camera_tables.py` | ✅ Done | cameras, camera_calibrations, camera_zones |
| 0.7.3 | Migration: frame tables | `services/persistence/alembic/versions/0002_create_frame_tables.py` | ✅ Done | frames, frame_quality_metrics |
| 0.7.4 | Migration: detection tables | `services/persistence/alembic/versions/0003_create_detection_tables.py` | ✅ Done | detections |
| 0.7.5 | Migration: tracking tables | `services/persistence/alembic/versions/0004_create_tracking_tables.py` | ✅ Done | tracks, track_history |
| 0.7.6 | Migration: ANPR tables | `services/persistence/alembic/versions/0005_create_anpr_tables.py` | ✅ Done | plate_reads, plate_candidates |
| 0.7.7 | Migration: incident/evidence/review tables | `services/persistence/alembic/versions/0006_create_incident_evidence_review_tables.py` | ✅ Done | violation_candidates, incidents, incident_scores, evidence_assets, review_actions |
| 1.1.1 | Create ingestion app entrypoint | `services/ingestion/app/main.py` | ✅ Done | create_app() factory |
| 1.1.2 | Create ingestion router | `services/ingestion/app/api/router.py` | ✅ Done | register_routes(app) |
| 1.1.3 | Create ingestion endpoints | `services/ingestion/app/api/endpoints.py` | ✅ Done | post_ingest_frame, get_camera_config |
| 1.2.1 | Create ingestion service | `services/ingestion/app/services/ingestion_service.py` | ✅ Done | validate → build record → publish job → orchestrate |
| 1.2.2 | Create object storage adapter | `services/ingestion/app/services/object_store.py` | ✅ Done | No queue publishing |
| 1.2.3 | Create queue publisher adapter | `services/ingestion/app/services/queue_publisher.py` | ✅ Done | No DB writes |
| 2.1.1 | Create preprocessing app entrypoint | `services/preprocessing/app/main.py` | ✅ Done | create_app() factory |
| 2.1.2 | Create preprocessing endpoint | `services/preprocessing/app/api/endpoints.py` | ✅ Done | post_preprocess_frame |
| 2.2.1 | Create image loader helpers | `libs/vision-utils/image_io.py` | ✅ Done | load, encode jpg/png |
| 2.2.2 | Create image color helpers | `libs/vision-utils/color_utils.py` | ✅ Done | bgr↔rgb, grayscale |
| 2.3.1 | Create blur score helper | `libs/vision-utils/quality_metrics.py` | ✅ Done | Laplacian variance |
| 2.3.2 | Add brightness score helper | `libs/vision-utils/quality_metrics.py` | ✅ Done | HSV V-channel mean |
| 2.3.3 | Add noise estimate helper | `libs/vision-utils/quality_metrics.py` | ✅ Done | MAD of Laplacian |
| 2.4.1 | Create lighting enhancement | `services/preprocessing/app/services/lighting_enhancement.py` | ✅ Done | CLAHE on LAB L-channel |
| 2.4.2 | Create denoise enhancement | `services/preprocessing/app/services/denoise_enhancement.py` | ✅ Done | Non-Local Means |
| 2.4.3 | Create resize normalization | `services/preprocessing/app/services/normalize_frame.py` | ✅ Done | Letterbox + color normalize |
| 2.5.1 | Create preprocessing orchestrator | `services/preprocessing/app/services/preprocess_service.py` | ✅ Done | analyze → plan → run |
| 3.1.1 | Create detection app main | `services/detection/app/main.py` | ✅ Done | create_app() factory |
| 3.1.2 | Create detection endpoint | `services/detection/app/api/endpoints.py` | ✅ Done | post_detect_frame |
| 3.2.1 | Create model loader | `services/detection/app/services/model_loader.py` | ✅ Done | Singleton ONNX stub |
| 3.3.1 | Create raw inference | `services/detection/app/services/inference.py` | ✅ Done | run_detection_inference |
| 3.3.2 | Create bbox helpers | `libs/vision-utils/bbox_utils.py` | ✅ Done | xyxy_to_dict, clip, center |
| 3.3.3 | Create detection formatter | `services/detection/app/services/format_results.py` | ✅ Done | extract, filter, build response |
| 3.4.1 | Create detection orchestrator | `services/detection/app/services/detection_service.py` | ✅ Done | detect_frame |
| 4.1.1 | Create tracking app main | `services/tracking/app/main.py` | ✅ Done | create_app() factory |
| 4.1.2 | Create tracking endpoint | `services/tracking/app/api/endpoints.py` | ✅ Done | post_track_frame |
| 4.2.1 | Create tracker loader | `services/tracking/app/services/tracker_loader.py` | ✅ Done | Singleton SORT stub |
| 4.2.2 | Create tracker update | `services/tracking/app/services/tracker_update.py` | ✅ Done | convert → update → output |
| 4.3.1 | Create motion features | `services/tracking/app/services/motion_features.py` | ✅ Done | motion vector, direction angle |
| 4.4.1 | Create tracking orchestrator | `services/tracking/app/services/tracking_service.py` | ✅ Done | track_frame |
| 5.1.1 | Create crop helpers | `libs/vision-utils/crop_utils.py` | ✅ Done | crop_bbox, expand, head region |
| 5.2.1 | Create rider association | `services/rule-engine/app/services/rider_association.py` | ✅ Done | IoU + overlap heuristics |
| 5.3.1 | Create helmet model loader | `services/rule-engine/app/services/helmet_model_loader.py` | ✅ Done | Singleton stub |
| 5.3.2 | Create helmet inference | `services/rule-engine/app/services/helmet_inference.py` | ✅ Done | classify + build candidate |
| 5.4.1 | Create helmet rule | `services/rule-engine/app/services/helmet_rule.py` | ✅ Done | extract → evaluate → run |
| 6.1.1 | Create plate detector loader | `services/anpr/app/services/plate_model_loader.py` | ✅ Done | Singleton stub |
| 6.1.2 | Create plate detection | `services/anpr/app/services/plate_detection.py` | ✅ Done | detect_plate_bbox, select_best |
| 6.2.1 | Create perspective helpers | `libs/vision-utils/perspective_utils.py` | ✅ Done | order_quad, warp_plate |
| 6.3.1 | Create OCR adapter | `services/anpr/app/services/ocr_adapter.py` | ✅ Done | PaddleOCR stub |
| 6.4.1 | Create plate text helpers | `services/anpr/app/services/plate_text.py` | ✅ Done | normalize, validate, rank |
| 6.5.1 | Create ANPR service | `services/anpr/app/services/anpr_service.py` | ✅ Done | read_plate orchestrator |
| 7.1.1 | Create score fusion | `services/incident-fusion/app/services/score_fusion.py` | ✅ Done | track stability, OCR reliability, weighted final |
| 7.2.1 | Create merge candidates | `services/incident-fusion/app/services/merge_candidates.py` | ✅ Done | group, merge labels, select primary |
| 7.3.1 | Create fusion service | `services/incident-fusion/app/services/fusion_service.py` | ✅ Done | fuse_incident orchestrator |
| 8.1.1 | Create annotation drawing | `services/evidence/app/services/draw_annotations.py` | ✅ Done | draw_bbox, header, plate text |
| 8.2.1 | Create evidence assets | `services/evidence/app/services/build_assets.py` | ✅ Done | thumbnail, annotated frame, manifest |
| 8.3.1 | Create evidence service | `services/evidence/app/services/evidence_service.py` | ✅ Done | generate_evidence orchestrator |
| 9.1.1 | Create dashboard app main | `services/dashboard-api/app/main.py` | ✅ Done | create_app() + CORS |
| 9.1.2 | Create dashboard endpoints | `services/dashboard-api/app/api/endpoints.py` | ✅ Done | get_incidents, get_by_id, post_review |
| 9.2.1 | Create incident query service | `services/dashboard-api/app/services/incident_queries.py` | ✅ Done | list, detail, save_review |

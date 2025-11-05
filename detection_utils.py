import json
from sqlalchemy.orm import Session
from models import DetectionHistory
from datetime import datetime
from disease_info import parse_disease_name

def save_detection(
    db: Session,
    user_id: int,
    image_name: str,
    predicted_class: str,
    confidence: float,
    top_3_predictions: list,
    notes: str = None
):
    """Save a detection result to the database"""
    crop_type, disease_name = parse_disease_name(predicted_class)
    
    top_3_json = json.dumps(top_3_predictions)
    
    detection = DetectionHistory(
        user_id=user_id,
        image_name=image_name,
        predicted_class=predicted_class,
        confidence=confidence,
        crop_type=crop_type,
        disease_name=disease_name,
        top_3_predictions=top_3_json,
        detection_date=datetime.utcnow(),
        notes=notes
    )
    
    db.add(detection)
    db.commit()
    db.refresh(detection)
    
    return detection

def get_user_detections(db: Session, user_id: int, limit: int = 50):
    """Get detection history for a user"""
    return db.query(DetectionHistory).filter(
        DetectionHistory.user_id == user_id
    ).order_by(
        DetectionHistory.detection_date.desc()
    ).limit(limit).all()

def get_user_stats(db: Session, user_id: int):
    """Get statistics for a user's detections"""
    detections = db.query(DetectionHistory).filter(
        DetectionHistory.user_id == user_id
    ).all()
    
    if not detections:
        return {
            'total_scans': 0,
            'crops_analyzed': {},
            'diseases_detected': {},
            'healthy_count': 0,
            'diseased_count': 0
        }
    
    crops_analyzed = {}
    diseases_detected = {}
    healthy_count = 0
    diseased_count = 0
    
    for detection in detections:
        crop_type = detection.crop_type
        disease_name = detection.disease_name
        
        crops_analyzed[crop_type] = crops_analyzed.get(crop_type, 0) + 1
        
        if 'healthy' in disease_name.lower():
            healthy_count += 1
        else:
            diseased_count += 1
            diseases_detected[disease_name] = diseases_detected.get(disease_name, 0) + 1
    
    return {
        'total_scans': len(detections),
        'crops_analyzed': crops_analyzed,
        'diseases_detected': diseases_detected,
        'healthy_count': healthy_count,
        'diseased_count': diseased_count
    }

def delete_detection(db: Session, detection_id: int, user_id: int):
    """Delete a detection (only if it belongs to the user)"""
    detection = db.query(DetectionHistory).filter(
        DetectionHistory.id == detection_id,
        DetectionHistory.user_id == user_id
    ).first()
    
    if detection:
        db.delete(detection)
        db.commit()
        return True
    return False

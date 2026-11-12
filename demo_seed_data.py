"""
Full System Seed & Demonstration Generator for AI-Based Road Accident Detection System (RADS).
Populates the database with realistic sample records across all 12 modules for live demonstration & viva presentation.
Run: py demo_seed_data.py
"""

import os
import sys
import django
from datetime import date, time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_accident.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files import File
from accident.models import Video, Prediction, Evidence, AccidentEvent, Alert
from accident.ai_model import detect_accident

def seed_full_demo():
    print("============================================================")
    print(" SEEDING DEMO DATA: ROAD ACCIDENT DETECTION SYSTEM (RADS)")
    print("============================================================")

    # 1. Get or create Admin user
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print(" [+] Created Admin account: admin / admin123")
    else:
        print(" [=] Found existing Admin account: admin")

    # 2. Get or create Standard User
    std_user, created = User.objects.get_or_create(username='user1')
    if created:
        std_user.set_password('user123')
        std_user.save()
        print(" [+] Created Standard User account: user1 / user123")
    else:
        print(" [=] Found existing Standard User account: user1")

    # Check sample video exists
    sample_video_path = "sample_traffic_feed.mp4"
    if not os.path.exists(sample_video_path):
        print(" [-] Sample video not found. Generating sample video...")
        import create_sample_video
        create_sample_video.generate_sample_video()

    # 3. Create Video Records
    print("\n [1/4] Populating Video Feeds (Module 3)...")
    v1, _ = Video.objects.get_or_create(
        video_name="NH-16 Highway Junction Cam 01",
        defaults={
            'source': 'Highway Camera',
            'uploaded_by': admin_user
        }
    )
    if not v1.video_file:
        with open(sample_video_path, 'rb') as f:
            v1.video_file.save("nh16_highway_junction.mp4", File(f), save=True)

    v2, _ = Video.objects.get_or_create(
        video_name="MG Road Commercial Intersection Cam 04",
        defaults={
            'source': 'CCTV Camera',
            'uploaded_by': admin_user
        }
    )
    if not v2.video_file:
        with open(sample_video_path, 'rb') as f:
            v2.video_file.save("mg_road_intersection.mp4", File(f), save=True)

    v3, _ = Video.objects.get_or_create(
        video_name="Expressway Flyover Feed 02",
        defaults={
            'source': 'Traffic Camera',
            'uploaded_by': admin_user
        }
    )
    if not v3.video_file:
        with open(sample_video_path, 'rb') as f:
            v3.video_file.save("expressway_flyover.mp4", File(f), save=True)

    print(f"  --> Created 3 Video Feeds (IDs: #{v1.video_id}, #{v2.video_id}, #{v3.video_id})")

    # 4. Create Predictions & Evidence
    print("\n [2/4] Generating AI Predictions & Evidence (Modules 5, 6 & 7)...")
    
    # Prediction 1: Confirmed Accident
    p1, _ = Prediction.objects.get_or_create(
        video=v1,
        defaults={
            'prediction': 'Accident',
            'confidence_score': 0.94,
            'verification_status': 'Confirmed'
        }
    )
    
    # Evidence 1 for Prediction 1
    ev1, _ = Evidence.objects.get_or_create(
        prediction=p1,
        defaults={
            'description': 'High-velocity collision detected at center lane junction with rapid motion anomaly.',
            'timestamp_in_video': '3.6s'
        }
    )

    # Prediction 2: Pending Verification
    p2, _ = Prediction.objects.get_or_create(
        video=v2,
        defaults={
            'prediction': 'Accident',
            'confidence_score': 0.88,
            'verification_status': 'Pending'
        }
    )
    ev2, _ = Evidence.objects.get_or_create(
        prediction=p2,
        defaults={
            'description': 'Vehicle abrupt deceleration and trajectory crossover detected.',
            'timestamp_in_video': '2.4s'
        }
    )

    # Prediction 3: Rejected False Detection
    p3, _ = Prediction.objects.get_or_create(
        video=v3,
        defaults={
            'prediction': 'No Accident',
            'confidence_score': 0.15,
            'verification_status': 'Rejected'
        }
    )

    print(f"  --> Created 3 AI Predictions: Confirmed (#{p1.prediction_id}), Pending (#{p2.prediction_id}), Rejected (#{p3.prediction_id})")

    # 5. Create Accident Event (Module 9)
    print("\n [3/4] Registering Official Accident Event (Module 9)...")
    event, created_ev = AccidentEvent.objects.get_or_create(
        prediction=p1,
        defaults={
            'location': 'NH-16 Highway, Near Rajamahendravaram Toll Plaza',
            'accident_date': date.today(),
            'accident_time': time(14, 30),
            'confidence_score': p1.confidence_score,
            'severity_level': 'High',
            'remarks': 'Multi-vehicle collision logged by system. Highway patrol unit dispatched.'
        }
    )
    print(f"  --> Official Accident Event #{event.accident_id} at '{event.location}' (Severity: {event.severity_level})")

    # 6. Create Emergency Alert (Module 10)
    print("\n [4/4] Dispatching Emergency Alert (Module 10)...")
    alert_msg = (
        f"CRITICAL ACCIDENT ALERT — High Severity | "
        f"Location: {event.location} | "
        f"Date: {event.accident_date} at {event.accident_time} | "
        f"AI Confidence: {event.confidence_percentage}% | "
        f"Incident ID: #{event.accident_id}"
    )
    alert, created_alt = Alert.objects.get_or_create(
        accident=event,
        defaults={
            'message': alert_msg,
            'status': 'Active'
        }
    )
    print(f"  --> Dispatched Emergency Alert #{alert.alert_id} (Status: {alert.status})")

    print("\n============================================================")
    print(" DEMO DATA SEEDING COMPLETE! ALL 12 MODULES OPERATIONAL.")
    print("============================================================")
    print(" You can now launch the Django server:")
    print("   py manage.py runserver")
    print(" And log in at http://127.0.0.1:8000/login/")
    print("   Admin Login: username='admin', password='admin123'")
    print("   User Login:  username='user1', password='user123'")
    print("============================================================")

if __name__ == '__main__':
    seed_full_demo()

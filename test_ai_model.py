"""
CLI Verification Script for Module 5: AI Accident Detection Component
Tests accident/ai_model.py on sample_traffic_feed.mp4 or any specified video file.
Run: python test_ai_model.py
"""

import os
import sys
import django

# Setup Django environment so ai_model can access settings.MEDIA_ROOT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_accident.settings')
django.setup()

from accident.ai_model import detect_accident

def run_test():
    sample_video = "sample_traffic_feed.mp4"
    if not os.path.exists(sample_video):
        print(f" Sample video '{sample_video}' not found in current folder.")
        print("Run 'python create_sample_video.py' first to create it.")
        return

    print("=" * 60)
    print(" TESTING MODULE 5: AI ACCIDENT DETECTION ENGINE")
    print(f" Target Video: {sample_video}")
    print("=" * 60)

    result = detect_accident(os.path.abspath(sample_video), video_id=999)

    print("\n DETECTION RESULTS:")
    print(f"  Prediction:             {result.get('prediction')}")
    print(f"  Confidence Score:       {result.get('confidence')} ({result.get('confidence_percentage')}%)")
    print(f"  Is Accident Flag:       {result.get('is_accident')}")
    print(f"  Evidence Timestamp:     {result.get('evidence_timestamp')}")
    print(f"  Evidence Frame Saved:   {result.get('evidence_frame_path')}")
    print(f"  Model Engine Used:      {result.get('model_type')}")
    print(f"  Total Frames Analyzed:  {result.get('frames_analyzed')}")
    print("=" * 60)
    print(" AI Detection Engine executed successfully!\n")

if __name__ == '__main__':
    run_test()

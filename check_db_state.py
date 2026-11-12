import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_accident.settings')
django.setup()

from accident.models import Video, Prediction, AccidentEvent
from accident.ai_model import detect_accident

print("=== CHECKING ALL VIDEOS IN DATABASE ===")
for v in Video.objects.all().order_by('video_id'):
    if os.path.exists(v.video_file.path):
        res = detect_accident(v.video_file.path, video_id=v.video_id)
        pred = res['prediction']
        conf = res['confidence_percentage']
        print(f"Video #{v.video_id}: '{v.video_name}' (uploaded by: {v.uploaded_by.username}) -> Actual AI: {pred} ({conf}%)")
        for p in v.predictions.all():
            has_ev = hasattr(p, 'accident_event')
            ev_id = p.accident_event.accident_id if has_ev else None
            print(f"    Saved Prediction #{p.prediction_id}: '{p.prediction}' ({p.confidence_percentage}%) | Status: {p.verification_status} | Event #{ev_id}")
    else:
        print(f"Video #{v.video_id}: '{v.video_name}' -> FILE NOT FOUND: {v.video_file.name}")

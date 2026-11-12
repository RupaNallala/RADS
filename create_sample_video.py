"""
Sample Traffic Video Generator for AI-Based Road Accident Detection System.
Generates a small 5-second sample MP4 traffic video to test video upload & preview.
Run: python create_sample_video.py
"""

import sys

def generate_sample_video():
    try:
        import cv2
        import numpy as np
    except ImportError:
        print(" OpenCV or NumPy is not installed yet.")
        print("Run: pip install opencv-python numpy")
        return

    output_filename = "sample_traffic_feed.mp4"
    width, height = 640, 360
    fps = 25
    duration_sec = 5
    total_frames = fps * duration_sec

    # Define video codec (mp4v works reliably on Windows)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    print(f" Generating sample video: {output_filename} ({width}x{height}, {fps} FPS, {duration_sec}s)...")

    for i in range(total_frames):
        # Create dark asphalt road background
        frame = np.full((height, width, 3), (40, 40, 45), dtype=np.uint8)

        # Draw green roadside borders
        cv2.rectangle(frame, (0, 0), (width, 50), (34, 139, 34), -1)
        cv2.rectangle(frame, (0, height - 50), (width, height), (34, 139, 34), -1)

        # Draw road lanes (dashed white line in center)
        lane_y = height // 2
        dash_offset = (i * 8) % 40
        for x in range(-dash_offset, width, 40):
            cv2.line(frame, (x, lane_y), (x + 20, lane_y), (255, 255, 255), 2)

        # Draw moving vehicle 1 (Blue car, moves left to right)
        car1_x = int((i * 6) % (width + 100)) - 50
        cv2.rectangle(frame, (car1_x, lane_y - 65), (car1_x + 70, lane_y - 25), (220, 50, 50), -1)
        cv2.putText(frame, "CAR 1", (car1_x + 5, lane_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Draw moving vehicle 2 (Yellow vehicle, moves right to left)
        car2_x = width - int((i * 5) % (width + 100))
        cv2.rectangle(frame, (car2_x, lane_y + 25), (car2_x + 80, lane_y + 65), (0, 215, 255), -1)
        cv2.putText(frame, "CAR 2", (car2_x + 5, lane_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

        # Add simulated CCTV timestamp overlay
        cv2.putText(frame, f"CCTV CAM-01 [SIMULATED] FRAME: {i:03d}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        out.write(frame)

    out.release()
    print(f" Sample video created successfully: '{output_filename}'")
    print(" You can now upload this file in the Video Upload portal to test Phase 2!")

if __name__ == '__main__':
    generate_sample_video()

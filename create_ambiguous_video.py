"""
Generates an ambiguous / uncertain traffic video for validation of RADS.
Simulates a vehicle swerving slightly or braking moderately without a collision or impact shock.
Produces borderline motion metrics (2.2 <= z < 2.8) to validate the Pending Review mechanism.
"""
import cv2
import numpy as np

def generate_ambiguous_video(output_filename="sample_ambiguous_traffic.mp4"):
    width, height = 640, 360
    fps = 25
    duration_sec = 4
    total_frames = fps * duration_sec

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    print(f"Generating ambiguous traffic video: {output_filename}...")

    car_x = 50
    lane_y = height // 2

    for i in range(total_frames):
        frame = np.full((height, width, 3), (40, 40, 45), dtype=np.uint8)

        # Green roadside
        cv2.rectangle(frame, (0, 0), (width, 50), (34, 139, 34), -1)
        cv2.rectangle(frame, (0, height - 50), (width, height), (34, 139, 34), -1)

        # Dashed lane
        for x in range(0, width, 40):
            cv2.line(frame, (x, lane_y), (x + 20, lane_y), (255, 255, 255), 2)

        # Moving vehicle with moderate swerve around frame 40-55
        if 40 <= i <= 55:
            car_x += 4
            car_y = lane_y - 25 - int(12 * np.sin((i - 40) / 15.0 * np.pi))
        else:
            car_x += 5
            car_y = lane_y - 25

        car_x_pos = int(car_x % (width + 80)) - 40
        cv2.rectangle(frame, (car_x_pos, car_y), (car_x_pos + 70, car_y + 35), (200, 100, 50), -1)
        cv2.putText(frame, "CAR", (car_x_pos + 10, car_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        cv2.putText(frame, f"CCTV AMBIGUOUS FEED [SEC: {i/fps:.2f}s]", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        out.write(frame)

    out.release()
    print(f"Generated ambiguous traffic video: {output_filename}")

if __name__ == '__main__':
    generate_ambiguous_video()

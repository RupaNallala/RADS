"""
Generates a realistic 5-second sample accident/collision video (MP4)
Simulates two vehicles approaching each other, colliding at an intersection,
stopping abruptly, and remaining stalled with wreckage on the road.
Used for benchmarking and validating the AI Road Accident Detection System.
"""
import cv2
import numpy as np

def generate_accident_sample_video(output_filename="sample_accident_collision.mp4"):
    width, height = 640, 360
    fps = 25
    duration_sec = 5
    total_frames = fps * duration_sec
    impact_frame = int(fps * 2.2)  # Impact at 2.2 seconds

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    print(f"Generating synthetic accident video: {output_filename}...")

    # Initial positions
    car1_x = 50
    car1_y = height // 2 - 20
    car2_x = width - 100
    car2_y = height // 2 - 20

    for i in range(total_frames):
        # Asphalt road background
        frame = np.full((height, width, 3), (40, 40, 45), dtype=np.uint8)

        # Green roadside
        cv2.rectangle(frame, (0, 0), (width, 50), (34, 139, 34), -1)
        cv2.rectangle(frame, (0, height - 50), (width, height), (34, 139, 34), -1)

        # Road lanes
        lane_y = height // 2
        for x in range(0, width, 40):
            cv2.line(frame, (x, lane_y), (x + 20, lane_y), (255, 255, 255), 2)

        if i < impact_frame:
            # Vehicles approaching each other in collision course
            car1_x += 6
            car2_x -= 6
            # Draw Vehicle 1 (Blue)
            cv2.rectangle(frame, (int(car1_x), car1_y - 20), (int(car1_x) + 70, car1_y + 20), (220, 50, 50), -1)
            cv2.putText(frame, "CAR 1", (int(car1_x) + 5, car1_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

            # Draw Vehicle 2 (Yellow)
            cv2.rectangle(frame, (int(car2_x), car2_y - 20), (int(car2_x) + 70, car2_y + 20), (0, 215, 255), -1)
            cv2.putText(frame, "CAR 2", (int(car2_x) + 5, car2_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
        elif i == impact_frame or i == impact_frame + 1:
            # Impact Moment: Violent collision displacement, flash & debris
            cv2.circle(frame, ((car1_x + car2_x) // 2 + 35, car1_y), 50, (0, 140, 255), -1)
            cv2.rectangle(frame, (int(car1_x), car1_y - 25), (int(car1_x) + 80, car1_y + 25), (200, 30, 30), -1)
            cv2.rectangle(frame, (int(car2_x), car2_y - 30), (int(car2_x) + 80, car2_y + 30), (0, 180, 230), -1)
            # Debris scatter
            np.random.seed(i)
            for _ in range(30):
                rx = int((car1_x + car2_x) // 2 + np.random.randint(-60, 60))
                ry = int(car1_y + np.random.randint(-40, 40))
                cv2.circle(frame, (rx, ry), np.random.randint(2, 6), (50, 50, 220), -1)
        else:
            # Post-Collision: Wrecked vehicles abruptly STOPPED and stationary on the road
            # Severe deformation, smoke/hazard
            cv2.rectangle(frame, (int(car1_x) + 5, car1_y - 15), (int(car1_x) + 75, car1_y + 15), (150, 40, 40), -1)
            cv2.rectangle(frame, (int(car2_x) - 10, car2_y - 25), (int(car2_x) + 65, car2_y + 20), (0, 150, 190), -1)
            cv2.putText(frame, "[COLLISION]", (int(car1_x) - 10, car1_y - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

        # CCTV timestamp overlay
        cv2.putText(frame, f"CCTV INTERSECTION CAM-02 [SEC: {i/fps:.2f}s]", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        out.write(frame)

    out.release()
    print(f"Generated synthetic accident video: {output_filename}")

if __name__ == '__main__':
    generate_accident_sample_video()

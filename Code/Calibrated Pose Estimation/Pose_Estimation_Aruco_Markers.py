"""
@file aruco_marker_detection.py
@brief This script implements ArUco marker generation, detection, and pose estimation using a Raspberry Pi and OpenCV.

@details
This project focuses on real-time ArUco marker tracking and pose estimation. It includes functionalities for:
- Generating ArUco markers.
- Detecting ArUco markers in real-time using the Raspberry Pi camera.
- Estimating marker pose relative to a dynamically updating origin marker.

@authors
- Conor Schott
- Gabriel Coria
- Emmanuel Baez
- Owen Guinane

@dependencies
- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- Picamera2 library

@date November 21, 2024
"""

from enum import Enum
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from picamera2 import Picamera2

class ArucoType(Enum):
    """
    @brief Enum class to define supported ArUco marker types.

    This enum provides predefined ArUco marker types that can be used for marker generation and detection.
    """
    DICT_4X4_50 = cv2.aruco.DICT_4X4_50
    DICT_4X4_100 = cv2.aruco.DICT_4X4_100
    DICT_4X4_250 = cv2.aruco.DICT_4X4_250
    DICT_4X4_1000 = cv2.aruco.DICT_4X4_1000
    DICT_5X5_50 = cv2.aruco.DICT_5X5_50
    DICT_5X5_100 = cv2.aruco.DICT_5X5_100
    DICT_5X5_250 = cv2.aruco.DICT_5X5_250
    DICT_5X5_1000 = cv2.aruco.DICT_5X5_1000
    DICT_6X6_50 = cv2.aruco.DICT_6X6_50
    DICT_6X6_100 = cv2.aruco.DICT_6X6_100
    DICT_6X6_250 = cv2.aruco.DICT_6X6_250
    DICT_6X6_1000 = cv2.aruco.DICT_6X6_1000
    DICT_7X7_50 = cv2.aruco.DICT_7X7_50
    DICT_7X7_100 = cv2.aruco.DICT_7X7_100
    DICT_7X7_250 = cv2.aruco.DICT_7X7_250
    DICT_7X7_1000 = cv2.aruco.DICT_7X7_1000
    DICT_ARUCO_ORIGINAL = cv2.aruco.DICT_ARUCO_ORIGINAL

class ArucoMarkers:
    """
    @class ArucoMarkers
    @brief Class to manage ArUco marker operations, including generation, detection, and pose estimation.

    @param marker_width_pixels The width of the marker in pixels. Default is 100 pixels.
    """
    def __init__(self, marker_width_pixels=100):
        """
        @brief Initializes the ArUcoMarkers object and configures the Raspberry Pi camera.

        @param marker_width_pixels The width of the marker in pixels. Default is 100 pixels.
        """
        self.dir = os.getcwd()  # Working directory
        self.piCam = Picamera2()  # Raspberry Pi Camera
        self.piCam.preview_configuration.main.size = (640, 480)
        self.piCam.preview_configuration.align()
        self.piCam.configure("preview")
        self.piCam.start()
        self.marker_width_pixels = marker_width_pixels  # Marker size in pixels
        self.origin_position = None  # Position of reference marker (Marker ID 1)
        self.smoothed_positions = {}  # Smoothed positions for each marker

    def generate_aruco_marker(self, aruco_type, marker_id, show_image=False):
        """
        @brief Generates and saves an ArUco marker as an image file.

        @param aruco_type The type of ArUco marker (from the ArucoType enum).
        @param marker_id The ID of the marker to generate.
        @param show_image Boolean flag to display the generated marker. Default is False.
        
        @note The marker is saved as `aruco_marker.png` in the current working directory.
        """
        print("Generating ArUco Marker...")
        aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_type.value)
        marker_image = np.zeros((self.marker_width_pixels, self.marker_width_pixels), dtype=np.uint8)
        marker_image = cv2.aruco.drawMarker(aruco_dict, marker_id, self.marker_width_pixels)

        # Add border around the marker
        border_width = 5
        marker_image = cv2.copyMakeBorder(
            marker_image,
            border_width, border_width, border_width, border_width,
            cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )
        cv2.imwrite(os.path.join(self.dir, "aruco_marker.png"), marker_image)

        if show_image:
            plt.imshow(marker_image, cmap="gray")
            plt.show()

    def aruco_marker_pose_estimation(self, aruco_type, camera_matrix, dist_coeffs):
        """
        @brief Detects ArUco markers in a live video stream, estimates their pose, and computes
               their position relative to a dynamic origin (Marker ID 1).

        @param aruco_type The type of ArUco marker (from the ArucoType enum).
        @param camera_matrix The camera matrix for intrinsic parameters.
        @param dist_coeffs The distortion coefficients for the camera.
        
        @note This function runs indefinitely, detecting and estimating the pose of ArUco markers 
              in real-time. Press `+` to increase the calibration factor, `-` to decrease, and `q` to quit.
        """
        print("Detecting ArUco Marker...")

        aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_type.value)
        aruco_params = cv2.aruco.DetectorParameters()

        marker_size_in_inches = 3.51
        calibration_factor = 2.754
        alpha_x = 0.05  # Smoothing factor for x-axis
        alpha_y = 0.65  # Smoothing factor for y-axis

        while True:
            frame = self.piCam.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Detect ArUco markers
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(frame_gray, aruco_dict, parameters=aruco_params)

            if ids is not None:
                frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

                for i, corner in enumerate(corners):
                    marker_id = ids[i][0]
                    center_x = int(np.mean(corner[0][:, 0]))
                    center_y = int(np.mean(corner[0][:, 1]))

                    if marker_id == 1:
                        self.origin_position = (center_x, center_y)

                    if self.origin_position is not None:
                        rel_x_pixels = center_x - self.origin_position[0]
                        rel_y_pixels = center_y - self.origin_position[1]

                        x_mm = rel_x_pixels * (marker_size_in_inches / (self.marker_width_pixels + 10)) * calibration_factor * 25.4
                        y_mm = rel_y_pixels * (marker_size_in_inches / (self.marker_width_pixels + 10)) * calibration_factor * 25.4

                        if marker_id not in self.smoothed_positions:
                            self.smoothed_positions[marker_id] = (x_mm, y_mm)
                        else:
                            prev_x, prev_y = self.smoothed_positions[marker_id]
                            x_mm = alpha_x * x_mm + (1 - alpha_x) * prev_x
                            y_mm = alpha_y * y_mm + (1 - alpha_y) * prev_y
                            self.smoothed_positions[marker_id] = (x_mm, y_mm)

                        print(f"Marker ID: {marker_id} - X: {x_mm:.2f} mm, Y: {y_mm:.2f} mm")

                        label = f"Marker {marker_id}"
                        coord_label = f"X: {x_mm:.2f} mm, Y: {y_mm:.2f} mm"
                        cv2.putText(frame, label, (center_x, center_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 0, 128), 1)
                        cv2.putText(frame, coord_label, (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 0, 128), 1)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            cv2.imshow("ArUco Marker Pose Estimation", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('+'):
                calibration_factor += 0.1
                print(f"Calibration Factor: {calibration_factor}")
            elif key == ord('-'):
                calibration_factor -= 0.1
                print(f"Calibration Factor: {calibration_factor}")

        cv2.destroyAllWindows()

if __name__ == "__main__":
    marker = ArucoMarkers()

    # Generate a marker
    marker.generate_aruco_marker(ArucoType.DICT_6X6_1000, 1, show_image=True)

    # Camera matrix and distortion coefficients
    camera_matrix = np.array([[535.4, 0, 320.1], [0, 539.2, 240.1], [0, 0, 1]], dtype=float)
    dist_coeffs = np.array([0.0, 0.0, 0.0, 0.0], dtype=float)

    # Start pose estimation
    marker.aruco_marker_pose_estimation(ArucoType.DICT_6X6_1000, camera_matrix, dist_coeffs)

"""
Senior Design Project: ArUco Marker Detection and Pose Estimation
===========================================================

Authors: 
- Conor Schott
- Gabriel Coria
- Emmanuel Baez
- Owen Guinane

Aruco Marker Detection and Pose Estimation
===========================================
This script detects ArUco markers in a video stream captured by a Raspberry Pi camera.
It calculates the relative position and orientation of detected markers with respect 
to a designated origin marker. The relative position is expressed in millimeters, and 
the orientation is given in degrees.

Key Features:
-------------
1. Real-time marker detection and pose estimation.
2. Dynamic origin setup using a specific marker (Marker ID 1).
3. Adjustable calibration factor for fine-tuning measurements.
4. Outputs marker position and orientation at a controlled 5 Hz rate.

Dependencies:
-------------
- Python 3.x
- OpenCV
- NumPy
- Picamera2 (for Raspberry Pi camera interface)

Notes:
------
- Press `+` or `-` to adjust the calibration factor during runtime.
- Press `q` to quit the detection process.
"""

import cv2
import numpy as np
import time
from picamera2 import Picamera2
import cv2.aruco as aruco

class ArucoMarkers:
    """
    Class for detecting ArUco markers and estimating their pose in real-time.

    This class utilizes the Raspberry Pi camera to detect ArUco markers in a video 
    stream, calculate their relative position and orientation with respect to a 
    designated origin marker (Marker ID 1), and display the results on the video stream.
    """

    def __init__(self, marker_width_pixels=100):
        """
        Constructor for the ArucoMarkers class.
        
        @param marker_width_pixels The width of the marker in pixels for scaling purposes.
        """
        # Initialize marker parameters and camera configuration
        self.marker_width_pixels = marker_width_pixels  # Width of the marker in pixels for scaling
        self.piCam = Picamera2()  # Initialize the Raspberry Pi camera
        self.piCam.preview_configuration.main.size = (640, 480)  # Set the camera resolution (640x480)
        self.piCam.preview_configuration.align()  # Ensure proper configuration alignment
        self.piCam.configure("preview")  # Configure the camera for preview mode
        self.piCam.start()  # Start the camera for capturing frames

        # Parameters for calibration and pose estimation
        self.marker_size_in_inches = 3.5  # Physical size of the marker in inches
        self.calibration_factor = 2.755  # Initial calibration factor for scaling purposes
        self.origin_position = None  # Store the position of the origin marker (Marker ID 1)
        self.origin_rotation_matrix = None  # Store the rotation matrix of the origin marker

        # Example camera calibration parameters: intrinsic camera matrix and distortion coefficients
        self.camera_matrix = np.array([
            [482.3, 0, 322.5],  # Focal lengths and principal point (cx, cy)
            [0, 486.2, 244.8],
            [0, 0, 1]
        ])
        self.dist_coeffs = np.array([0.1, -0.02, 0, 0, 0])  # Distortion coefficients for the camera

    def detect_aruco_markers(self, aruco_type=aruco.DICT_6X6_100):
        """
        Detects ArUco markers in the camera's video stream and calculates their pose 
        relative to the origin marker (Marker ID 1).
        
        @param aruco_type Predefined ArUco dictionary type (default: DICT_6X6_100).
        """
        # Load the ArUco dictionary and set the detection parameters
        aruco_dict = aruco.getPredefinedDictionary(aruco_type)  # Predefined ArUco dictionary
        aruco_params = aruco.DetectorParameters()  # Default ArUco detection parameters

        # Define 3D coordinates of the marker corners in the world frame
        world_points = np.array([
            [0., 0., 0.],  # Bottom-left corner
            [1., 0., 0.],  # Bottom-right corner
            [1., 1., 0.],  # Top-right corner
            [0., 1., 0.]   # Top-left corner
        ])

        # Timer to control output frequency (5 Hz)
        last_print_time = time.time()

        while True:
            # Capture a frame from the camera and convert it to grayscale
            frame = self.piCam.capture_array()  # Capture an image from the Pi camera
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert the image to BGR format (OpenCV standard)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for ArUco detection

            # Detect markers in the frame
            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

            if ids is not None:  # If markers are detected
                # Draw detected markers on the frame
                frame = aruco.drawDetectedMarkers(frame, corners, ids)

                # Iterate through all detected markers
                for i, corner in enumerate(corners):
                    marker_id = ids[i][0]  # Extract the marker ID
                    # Solve the PnP problem to estimate pose (rotation and translation)
                    _, rvec, tvec = cv2.solvePnP(world_points, corner[0], self.camera_matrix, self.dist_coeffs)

                    # Calculate the center of the marker
                    center_x = int(np.mean(corner[0][:, 0]))  # Average x-coordinate of the marker corners
                    center_y = int(np.mean(corner[0][:, 1]))  # Average y-coordinate of the marker corners

                    # Set the origin marker (Marker ID 1) for relative calculations
                    if marker_id == 1:
                        self.origin_position = (center_x, center_y)  # Set origin position as the center of marker 1
                        self.origin_rotation_matrix, _ = cv2.Rodrigues(rvec)  # Store the origin's rotation matrix

                    if self.origin_position is not None and self.origin_rotation_matrix is not None:
                        # Calculate the relative position in pixels, then convert to mm
                        rel_x_pixels = center_x - self.origin_position[0]
                        rel_y_pixels = center_y - self.origin_position[1]
                        x_mm = rel_x_pixels * (self.marker_size_in_inches / self.marker_width_pixels) * self.calibration_factor * 25.4
                        y_mm = rel_y_pixels * (self.marker_size_in_inches / self.marker_width_pixels) * self.calibration_factor * 25.4

                        # Compute the relative rotation angle using Rodrigues' formula
                        current_rotation_matrix, _ = cv2.Rodrigues(rvec)
                        relative_rotation_matrix = np.dot(current_rotation_matrix, self.origin_rotation_matrix.T)
                        angle_rad = np.arccos((np.trace(relative_rotation_matrix) - 1) / 2)
                        angle_deg = np.degrees(angle_rad)

                        # Print marker information at a 5 Hz rate (every 0.2 seconds)
                        current_time = time.time()
                        if current_time - last_print_time >= 0.2:
                            print(f"Marker ID: {marker_id} - X: {x_mm:.2f} mm, Y: {y_mm:.2f} mm, Angle: {angle_deg:.2f}°")
                            last_print_time = current_time

                        # Display marker position and orientation on the frame
                        label = f"ID {marker_id} | X: {x_mm:.2f} mm, Y: {y_mm:.2f} mm, Angle: {angle_deg:.2f}°"
                        cv2.putText(frame, label, (center_x, center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                    # Draw coordinate axes for each detected marker
                    cv2.drawFrameAxes(frame, self.camera_matrix, self.dist_coeffs, rvec, tvec, 1)

                # Handle runtime calibration adjustments and exit command
                key = cv2.waitKey(1) & 0xFF
                if key == ord('+'):  # Increase calibration factor
                    self.calibration_factor += 0.1
                elif key == ord('-'):  # Decrease calibration factor
                    self.calibration_factor = max(0.1, self.calibration_factor - 0.1)
                elif key == ord('q'):  # Exit the detection loop
                    break

            # Display the video frame with detected markers and pose information
            cv2.imshow('Aruco Detection', frame)

        # Clean up resources after exiting
        self.piCam.stop()  # Stop the Pi camera
        cv2.destroyAllWindows()  # Close the OpenCV window


# Example usage of the ArucoMarkers class
if __name__ == "__main__":
    # Create an instance of the ArucoMarkers class
    aruco_markers = ArucoMarkers()
    # Start the marker detection process
    aruco_markers.detect_aruco_markers()


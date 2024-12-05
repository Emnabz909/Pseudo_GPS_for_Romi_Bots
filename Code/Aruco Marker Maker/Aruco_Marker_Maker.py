"""
Senior Design Project: ArUco Marker Generation
=================================================

Authors: 
- Conor Schott
- Gabriel Coria
- Emmanuel Baez
- Owen Guinane

Aruco Marker Generation
=======================
This script generates ArUco markers of a specified dictionary type and ID, labels each marker with its unique ID, 
and saves them as image files in the current directory. The ArUco markers are commonly used for computer vision 
applications such as pose estimation, object tracking, and calibration tasks in robotics and other fields.

Key Features:
-------------
1. Generate ArUco markers of a specified dictionary type (currently supports DICT_6X6_250).
2. Customizable marker size in pixels, with an adjustable border width for visibility.
3. Labels each marker with its unique ID and saves them as PNG files.
4. Easy to scale for generating multiple markers in a batch.

Dependencies:
-------------
- Python 3.x
- OpenCV (for ArUco marker generation and image processing)
- NumPy (for matrix handling and image manipulation)
- OS (for file and directory handling)

Notes:
------
- The generated markers will be saved in the same directory where the script is executed.
- Currently, only the DICT_6X6_250 ArUco dictionary is supported, but it can be extended to other dictionaries.
- The script can be customized to generate any number of markers by adjusting the `marker_count` parameter.
- The marker size can be set by changing the `marker_width_pixels` parameter.

"""
# Import necessary libraries
from enum import Enum
import cv2
import numpy as np
import os

# Enum class to define available ArUco marker dictionaries
class ArucoType(Enum):
    """
    Enum class for supported ArUco marker dictionaries.

    Currently supports DICT_6X6_250, which is a predefined set of ArUco markers with 6x6 grids and 250 unique IDs.
    """
    DICT_6X6_250 = cv2.aruco.DICT_6X6_250  # Dictionary with 6x6 markers and 250 unique IDs

# Class to generate and save ArUco markers
class ArucoMarkers:
    """
    Class for generating and saving ArUco markers.
    
    This class handles the generation of ArUco markers, adds borders, labels them with their unique IDs, 
    and saves the markers as image files.
    """
    
    def __init__(self):
        """
        Constructor for the ArucoMarkers class.
        
        Initializes the object by determining the directory where the script is located.
        This will be used to save the generated marker images.
        """
        self.dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of the script
    
    def generate_aruco_marker(self, aruco_type, marker_id, marker_width_pixels):
        """
        Generates a single ArUco marker, adds a border and label, and saves it as a PNG image.
        
        Args:
            aruco_type (ArucoType): The ArUco dictionary type to use (e.g., DICT_6X6_250).
            marker_id (int): The unique ID of the marker to generate.
            marker_width_pixels (int): The size of the marker in pixels (excluding borders).
        """
        # Print message about the current marker being generated
        print(f'Generating ArUco Marker ID: {marker_id}...')
        
        # Get the ArUco dictionary based on the selected type (e.g., DICT_6X6_250)
        aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_type.value)
        
        # Create an empty black image to hold the marker
        marker_image = np.zeros((marker_width_pixels, marker_width_pixels), dtype=np.uint8)
        
        # Generate the ArUco marker using the specified dictionary and marker ID
        marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_width_pixels, marker_image, 1)
        
        # Add a white border around the generated marker for better visibility
        border_width = 5  # Width of the border in pixels
        marker_image = cv2.copyMakeBorder(
            marker_image,
            border_width, border_width, border_width, border_width,
            cv2.BORDER_CONSTANT,
            value=[255, 255, 255]  # Set border color to white
        )
        
        # Set parameters for adding text to the marker (labeling with its ID)
        font = cv2.FONT_HERSHEY_SIMPLEX  # Font style for the label
        font_scale = 1  # Font scale for the label
        font_color = (0, 0, 0)  # Text color (black)
        thickness = 2  # Line thickness for the text
        text = str(marker_id)  # Convert marker ID to a string for display
        
        # Calculate the size of the text to center it on the marker
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (marker_image.shape[1] - text_size[0]) // 2  # Center horizontally
        text_y = marker_image.shape[0] - 10  # Position text towards the bottom with some margin
        
        # Draw the text (marker ID) on the marker image
        cv2.putText(marker_image, text, (text_x, text_y), font, font_scale, font_color, thickness)
        
        # Define the output path for saving the marker image
        output_path = os.path.join(self.dir, f'aruco_marker_{marker_id}.png')
        
        # Save the generated marker image as a PNG file in the current directory
        cv2.imwrite(output_path, marker_image)
        
        # Print confirmation message about where the marker was saved
        print(f"Marker ID {marker_id} saved at: {output_path}")

# Function to generate multiple ArUco markers
def generate_markers(aruco_type, marker_count, marker_width_pixels):
    """
    Generates and saves multiple ArUco markers.

    Args:
        aruco_type (ArucoType): The ArUco dictionary type to use (e.g., DICT_6X6_250).
        marker_count (int): The number of markers to generate.
        marker_width_pixels (int): The size of each marker in pixels (excluding borders).
    """
        # Print message about how many markers will be generated
        print(f"Generating {marker_count} ArUco markers of type {aruco_type.name}...")
        
        # Create an instance of the ArucoMarkers class to handle marker generation
        aruco_marker = ArucoMarkers()
        
        # Loop to generate and save each marker with a unique ID
        for marker_id in range(1, marker_count + 1):
            aruco_marker.generate_aruco_marker(aruco_type, marker_id, marker_width_pixels)
        
        # Print confirmation message when all markers are generated
        print("All markers generated successfully!")

# Main script execution starts here
if __name__ == '__main__':
    """
    Main entry point for the script. This section is responsible for calling the function
    to generate ArUco markers.
    
    Generates 20 markers of type DICT_6X6_250, with a size of 200x200 pixels (excluding borders).
    """
    generate_markers(ArucoType.DICT_6X6_250, marker_count=20, marker_width_pixels=200)

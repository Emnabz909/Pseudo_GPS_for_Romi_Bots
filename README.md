# Pseudo_GPS_for_Romi_Bots
Senior Project for Charlie Refvem by Emmanuel Baez, Gabriel Coria, Owen Guinane and Conor Schott

## Table of Contents
[Statement of Disclaimer](#statement-of-disclaimer)<br>
[Project Overview](#project-overview)<br>
[Concept Description and Justification](#concept-description-and-justification)<br>

## Statement of Disclaimer
Since this project is a result of a class assignment, it has been graded and accepted as a fulfillment of the course requirements. Acceptance does not imply technical accuracy or reliability. Any use of information in this report is at risk to the user. These risks may include catastrophic failure of the device or infringement of patent or copyright laws. California Polytechnic State University at San Luis Obispo and its staff cannot be held liable for any use or misuse of the project.   

## Project Overview
This project aims to develop a "pseudo-GPS" system that provides real-time, accurate location data to multiple Romi robots within a lab environment, since traditional GPS is ineffective indoors. Indoor localization technologies such as radar, ultrasonic sensors, and camera vision systems could offer valuable insights for this endeavor. Currently, ME 405 students work with Romi robots but lack access to absolute orientation and location data, which would enhance algorithm development. The design challenge is to create a prototype sensor to help students perform localization tasks more effectively. Key objectives include developing and testing a functional prototype by Fall 2024 if feasible, analyzing and documenting its accuracy, range, update rate, and latency, and providing comprehensive schematics and well-documented code to ensure the project can be continued seamlessly in the future. 

## Concept Description and Justification 
Mounted overhead, the camera captures images of the lab table, which are processed to generate a grid overlay in 2-dimensional space, facilitating precise localization and differentiation of objects. The device creates an origin point on the table, which it uses to measure Romi bots and obstacles relative to it. It constantly monitors Romi bots and obstacles within its field of view. Data such as grid representation and object positioning are handled by our microcontroller for processing. 

To aid the microcontroller with processing, we will develop custom libraries tailored to recognize specific objects in the environment, including the Romi robots, table, and obstacles. Instead of training models through Teachable Machine, we will use Aruco markers, which function similarly to QR codes, to identify and track each object. 

We are confident that our hardware will be able to meet the project specifications. By using trigonometry and the manufacturer-given data on the camera modules, we can estimate an accuracy of 0.55 mm per pixel for the Raspberry Pi Camera Module 3 and an accuracy of 1mm per pixel with the Raspberry Pi Camera Module 3, assuming a mounting height of 6.75ft above the table. This falls well-within our target accuracy of +- 5mm for Romi tracking. 

# Pseudo_GPS_for_Romi_Bots
Senior Project for Charlie Refvem by Emmanuel Baez, Gabriel Coria, Owen Guinane and Conor Schott

## Table of Contents
[Statement of Disclaimer](#statement-of-disclaimer)<br>
[Project Overview](#project-overview)<br>
[Concept Description and Justification](#concept-description-and-justification)<br>

## Statement of Disclaimer
Since this project is a result of a class assignment, it has been graded and accepted as a fulfillment of the course requirements. Acceptance does not imply technical accuracy or reliability. Any use of information in this report is at risk to the user. These risks may include catastrophic failure of the device or infringement of patent or copyright laws. California Polytechnic State University at San Luis Obispo and its staff cannot be held liable for any use or misuse of the project.   

## Project Overview
We have finalized the concept selection and are currently expanding further iterations on our concept prototype. This report aims to describe our chosen concept, our reasoning behind it, and a table of the alternate solutions considered. In addition, this report also includes a preliminary analysis, a weighted design matrix, an updated Gantt chart, a design hazard matrix, and our references. We hope to get feedback on our reasoning for the sensor choice and on the housing system.   

For our system, we decided to use a Raspberry Pi with a camera to obtain absolute orientation and positional data. The basic layout is depicted in Figure 1 below. 


## Concept Description and Justification 
Mounted overhead, the camera captures images of the lab table, which are processed to generate a grid overlay in 2-dimensional space, facilitating precise localization and differentiation of objects. The device creates an origin point on the table, which it uses to measure Romi bots and obstacles relative to it. It constantly monitors Romi bots and obstacles within its field of view. Data such as grid representation and object positioning are handled by our microcontroller for processing. 

To assist the microcontroller with processing, we will create custom libraries that will reference our specific objects, such as the Romi bots, table, and obstacles. These libraries will be created and trained through an online AI software called Teachable Machine developed by Google. Orientation of Romi bots could also be achieved if they had unique identifiers on their circular base plate, such as N, S, E, W signs or a 3D printed arrow. 

We are confident that our hardware will be able to meet the project specifications. By using trigonometry and the manufacturer-given data on the camera modules, we can estimate an accuracy of 0.55 mm per pixel for the Raspberry Pi Camera Module 3 and an accuracy of 1mm per pixel with the Raspberry Pi Camera Module 3, assuming a mounting height of 6.75ft above the table. This falls well-within our target accuracy of +- 5mm for Romi tracking. 

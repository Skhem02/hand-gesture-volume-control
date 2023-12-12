# Hand Gesture Volume Control with OpenCV and Mediapipe

This Python script uses OpenCV and Mediapipe to detect hand gestures and control system volume based on the distance between the thumb and index finger. Additionally, it displays the hand landmarks and their connections in real-time.

## Features

- Hand gesture recognition for volume control.
- Real-time visualization of hand landmarks and connections.
- Adjustable volume range.

## How It Works

1. **Initialization**: The script initializes the webcam, hand tracking, and audio interface for volume control.

2. **Hand Tracking**: OpenCV and Mediapipe are used to detect and track hand landmarks in real-time.

3. **Gesture Recognition**: The distance between the thumb and index finger is calculated, and gestures are recognized based on this distance.

4. **Volume Control**: The calculated distance is mapped to the system volume range, and the volume is adjusted accordingly using the Pycaw library.

5. **Visualization**: The script provides visual feedback by displaying hand landmarks, connections, and a volume indicator on the screen.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- Numpy
- Pycaw

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Skhem02/hand-gesture-volume-control.git

## Install the required packages:

   ```bash
  pip install opencv-python mediapipe numpy pycaw

# Hexapod Robotics Code

This repository contains code for the Artificial Intelligence Club at PCC's Hexapod Robot project. The codebase is primarily written in Python for GUI and control system, with some C++ components in Arduino for performance-critical tasks. Our goal is to develop robust, intelligent control software for a six-legged (hexapod) robot platform.

## Features

- Modular Python architecture for easy development and experimentation
- C++ modules for efficient, low-level hardware interfacing
- Gait control and movement algorithms for hexapod locomotion 
- Sensor integration and data processing (To be implemented)
- Extensible design for adding new behaviors or sensors

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git
- Arduino IDE (for uploading .ino code to microcontroller) 
- (Optional) Hardware: Hexapod robot platform, compatible microcontroller, and sensors

### Clone the Repository

```bash
git clone https://github.com/Artificial-Intelligence-Club-at-PCC/robotics.git
cd robotics
```

### 1. Running the Main Python Program

To start the main robot control loop, run:

```bash
python main.py
```

This will launch the primary control interface for the hexapod robot. Additional command-line arguments or configuration files may be required depending on your setup; check the documentation in other project files for customization.

### 2. Uploading the Arduino Program

If your hexapod robot uses an Arduino (or compatible microcontroller) for motor control or sensor interfacing, you will need to upload the corresponding Arduino sketch:

1. **Locate the Arduino Code**: Find the `.ino` file (Arduino sketch) in the repository.

2. **Open in Arduino IDE**: Launch the [Arduino IDE](https://www.arduino.cc/en/software/) and open the `.ino` file.

3. **Connect Your Arduino Board**: Plug in your Arduino via USB or via Wifi by following the instructions given in the tutorials for the hexapod.

4. **Select Board and Port**: In the IDE, go to `Tools > Board` and select your Arduino model. Then select the correct port under `Tools > Port`.

5. **Upload the Sketch**: Click the Upload button (right arrow icon) or select `Sketch > Upload`.

6. **Verify Upload**: The status bar should indicate a successful upload. Once complete, your Arduino should be running the robot's firmware.

> _For more advanced setups, such as communication between Python and Arduino (e.g., via serial port), ensure that port settings in your Python code match your Arduino's configuration._


---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements, bug fixes, or new features.

---

## License

This project is maintained by the Artificial Intelligence Club at PCC.

---

## Contact

For questions or suggestions, please reach out to the club project leader!

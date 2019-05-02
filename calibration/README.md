# Force Sensor Calibration

## Description
- The goal of the calibration on force sensor is to generate a formula that could convert the voltage signal coming from force sensor to actual torque applied on such sensor. Such relationship will be used whenever analyze on actual torque applied on sensor is required. The relationship is expected to be varied in minor ranges based on temperature, humidity and long time of constant usage of sensor. Such calibration is necessary to be re-proceed once environment of torque sensor is changed. This section reports one test trail of calibration process.


## Test Hardware 
- Torque Sensor: Futek TFF600
- Amplifier: Omega DMD465WB
- DAQ (data acquisition card): NI USB

## Data pipeline
![calibration_pipline.jpg]()
- Amplifier takes power supply from 110V (wall), and also supply power for torque sensor by 10V through `B-` & `B+` channels.
- Gain of amplifier tested is around 250.
- `Ni data acquisition toolbox` or `Simulink data acquisition` of MatLab can be used to acquisite numerical voltage data from software end.
- 

  
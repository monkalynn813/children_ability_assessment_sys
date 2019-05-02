# Force Sensor Calibration

## Description
- The goal of the calibration on force sensor is to generate a formula that could convert the voltage signal coming from force sensor to actual torque applied on such sensor. Such relationship will be used whenever analyze on actual torque applied on sensor is required. The relationship is expected to be varied in minor ranges based on temperature, humidity and long time of constant usage of sensor. Such calibration is necessary to be re-proceed once environment of torque sensor is changed. This section reports one test trail of calibration process.


## Test Hardware 
- Torque Sensor: Futek TFF600
- Amplifier: Omega DMD465WB
- DAQ (data acquisition card): NI USB

## Data pipeline
![calibration_pipline.jpg](https://github.com/monkalynn813/children_ability_assessment_sys/blob/master/calibration/img/calibration_pipeline.jpg)
- Amplifier takes power supply from 110V (wall), and also supply power for torque sensor by 10V through `B-` & `B+` channels.
- Gain of amplifier tested is around 250.
- `Ni data acquisition toolbox` or `Simulink data acquisition` of MatLab can be used to receive numerical voltage data from software end.

## Calibration detail
#### Hardware setup
- Torque sensor was placed vertically with base mounted to a vertical surface.
- A rigid metal bar with small notch on one end was mounted to force sensor.
- An incremented weight from 0 to 75 lbs was placed at notch.
#### process
- voltage data was read through acquisition tool in unit of `Volt` with weight applied increases from 0 to 75 lbs, and back to 0 lbs.
- Actual torque applied on the sensor is computed with length of notch (`52cm`) to the sensor and weight applied at notch in unit of `N-m`.
- A linear regression method was applied based on data points of `actual torque (N-m)` vs. `Voltage data (Volt)`, corresponding model was generated and saved for future use.

#### extra comment
- level tool was used to make sure the sensor was placed vertically and notch side of bar is at horizontal level.
- Voltage data with 0 weight at notch was applied again after applied 75 lbs to check if the force sensor was able to recover function in a short time.
- The range of 0 to 75 lbs was used in this process since human may most likely generate force in such range.
- The none-zero voltage data with 0 weight applied at notch may not need a compensation in such formula since all measurement is relative to such baseline.

## Sample Calibration Data and Result


  
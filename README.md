# children_ability_assessment_sys
## Engineering Journal
#### Jingyan Ling

## 09/25 - 09/30/2019

- NI-data acquisition card with ROS
- Add dependency: nidaqmx (python package)


- Filtered data:
  - INFO NEEDED: NI-DAQ card sample rate (fs)
  - determine moving window size
  - determine filtered data update frequency
  
- TODO:
  - Add ROS customize message type for multiple channel data
  - plot using RQT

## 09/24/2019

- ROS with Windows
  - Visual Studio 2019 version has been changed on the windows machine
  - The shortcut of `cmd` has been changed from `...\Community\...` to `...\Professional\...`
- Shortcut has been tested and able to run `rosnode`
  - `publisher` works with a sample string
- Potential Issues:
  - Any `ros` command responses much slower than before, check if there will be a lag issue when do data streaming.
  - The directory has to be changed to the executable to run the node.
  
- Re-arrange github to update scripts from Linux and Windows 
  - Keep the `build` and `devel` of `ROS` locally
  - `git pull` to update scripts only
  - Check `gitignore` for detail
- To run package from windows machine:
  - Now shares the same repo as Linux version
  - Need to source the `...\devel\setup.bat` every time

- TODO
  - Implement the NI-data acquisition card python API to a `rosnode`
# children_ability_assessment_sys
## Engineering Journal
#### Jingyan Ling

## 09/24/2019

- ROS with Windows
  - Visual Studio 2019 version has been changed on the windows machine
  - The shortcut of `cmd` has been changed from `...\Community\...` to `...\Professional\...`
  - Add the following target to the `ROS` shortcut
  ~~~
  &&C:\Users\pthms\Desktop\ling\force_ws\devel\setup.bat
  ~~~
- Shortcut has been tested and able to run `rosnode`
  - `publisher` works with a sample string
- Potential Issues:
  - Any `ros` command is slower than before, check if there will be a lag issue when do data streaming.
  - The directory has to be changed to the executable to run the node.
  
  
- Implement the NI-data acquisition card python API to a `rosnode`
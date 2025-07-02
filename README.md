


# my_bot



# dependencies
Dependencies an required packages can be installed using scripts from "config".

*install_dependencies.py* should be run on dev machine.

*install_dependencies_bot.py* should be run on robot itself.


# Launch files
- **rsp.launch.py** - Base launch file for simulation, creates robot description and robot_state_publisher.
- **launch_sim.launch.py** - File for launching robot simulation, launches *rsp.launch.py* and Gazebo.
- **mapping_sim.launch.py** - File for simulating mapping with the robot using slam_toolbox
- **rplidar_bot.launch.py** - File meant to be run on robot itself. Launches rplidar driver that publishes Scan msgs.
- **launch_sim_control.launch.py** - File for launching simulation with ros2 control. For teleop driving topic /cmd_vel must be remapped to /diff_cont/cmd_vel_unstamped

```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

```


# Serial motor demo
Install the following package in your workspace on both dev machine and the robot:

```
git clone https://github.com/joshnewans/serial_motor_demo.git
```

build with colcon and source.

The github page of the package can be found [here](https://github.com/joshnewans/serial_motor_demo)

## Testing functionality
**On robot (ssh) run**

```
ros2 run serial_motor_demo driver --ros-args -p serial_port:=<your_serial_port> -p baudrate:=57600 -p loop_rate:=30 -p encoder_cpr:=3450
```
*Note:* Set the right serial port, usually /dev/ttyACM0 or /dev/ttyUSB0

**On dev machine**
```
ros2 run serial_motor_demo gui
```

## Manual control
Install python serial terminal
```
pip3 install pyserial
```
Run miniterm
```
python3 -m serial.tools.miniterm /dev/ttyACM0 57600
```
Set the serial port!

Refer to this repo for instructions [ros-arduino bridge](https://github.com/joshnewans/ros_arduino_bridge/blob/main/README.md)

## ROS - Arduino bridge
Download arduino firmware [here](https://github.com/joshnewans/ros_arduino_bridge/tree/main) and flash it on the Arduino.
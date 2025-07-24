from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_tutorials',
            executable='move_robot_action_server',
            name='move_robot_server',
            output='screen',
            emulate_tty=True,  #stands for TeleTypeWriter - behaving as if script was ran in terminal
        ),

        Node(
            package='ros2_tutorials',
            executable='rotation_action_server',
            name='rotate_robot_server',
            output='screen',
            emulate_tty=True,  #stands for TeleTypeWriter - behaving as if script was ran in terminal
        )
    ])
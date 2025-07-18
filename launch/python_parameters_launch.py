from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_tutorials',
            executable='minimal_param_node',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,  #stands for TeleTypeWriter - behaving as if script was ran in terminal
            parameters=[
                {'my_parameter': 'earth'}
            ]
        )
    ])
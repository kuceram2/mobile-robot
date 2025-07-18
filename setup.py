from setuptools import find_packages, setup

package_name = 'ros2_tutorials'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='guest',
    maintainer_email='skokankucera@seznam.cz',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = ros2_tutorials.publisher_member_function:main',
            'listener = ros2_tutorials.subscriber_member_function:main',
            'lidar_listener = ros2_tutorials.lidar_subscriber:main',
            'cmd_vel_publisher = ros2_tutorials.publisher_robot_driver:main',
            'obstacle_detection = ros2_tutorials.obstacle_detection:main',
            'add_ints_srv = ros2_tutorials.service_member_function:main',
            'add_ints_client = ros2_tutorials.client_member_function:main',
        ],
    },
)

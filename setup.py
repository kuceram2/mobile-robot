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
            'talker = py_pubsub.publisher_member_function:main',
            'listener = py_pubsub.subscriber_member_function:main',
            'lidar_listener = py_pubsub.lidar_subscriber:main',
            'cmd_vel_publisher = py_pubsub.publisher_robot_driver:main',
            'obstacle_detection = py_pubsub.obstacle_detection:main',
        ],
    },
)

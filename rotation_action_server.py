import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist

import time

#from action_tutorials_interfaces.action import Fibonacci
from tutorial_interfaces.action import Rotate

class RotationActionServer(Node):

    def __init__(self):
        super().__init__('rotate_action_server')
        self._action_server = ActionServer(
            self,
            Rotate, #interface name
            'rotate', # action name (both must match with action client)
            self.execute_callback)
        
        # subscriber for getting current rotation
        self.subscription = self.create_subscription(Vector3, 'orientation_euler', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self.current_angle = 0.0
        self.accumulated_angle = 0.0

        # publisher for commanding the robot
        self.publisher_ = self.create_publisher(Twist, 'diff_cont/cmd_vel_unstamped', 10)

    # Update accumulated angle with wrap-around correction
    def update_continuous_angle(self, current_angle, last_angle, accumulated_angle):
        delta = current_angle - last_angle
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        accumulated_angle += delta
        return accumulated_angle
    
    # Rotate relative: returns target and updated state
    def rotate_relative(self, accumulated_angle, relative_rotation):
        return accumulated_angle + relative_rotation

    def listener_callback(self, msg):
        self.current_angle = msg.z
    

    def execute_callback(self, goal_handle):
        desired_rotation = goal_handle.request.goal
        feedback_msg = Rotate.Feedback()
        last_angle = self.current_angle
        goal = self.current_angle + desired_rotation
        cmd_msg = Twist()
        if desired_rotation > 0: cv = False
        else: cv = True
        angle = self.accumulated_angle
        target_angle = self.rotate_relative(self.accumulated_angle, desired_rotation)

        while True:
            self.accumulated_angle = self.update_continuous_angle(self.current_angle, last_angle, self.accumulated_angle)
            last_angle = self.current_angle

            direction = 1 if desired_rotation > 0 else -1

            cmd_msg.angular.z = 0.2 * direction
            self.publisher_.publish(cmd_msg)
            time.sleep(0.1)

            if (desired_rotation > 0 and self.accumulated_angle >= target_angle) or \
            (desired_rotation < 0 and self.accumulated_angle <= target_angle):
                break

        cmd_msg.angular.z = 0.0
        self.publisher_.publish(cmd_msg)
            
        goal_handle.succeed()
        result = Rotate.Result()
        result.result = "Done!"
        self.get_logger().info(f'Result: {result.result}')
        return result


def main(args=None):
    rclpy.init(args=args)

    rotate_action_server = RotationActionServer()

    executor = MultiThreadedExecutor()
    executor.add_node(rotate_action_server)
    executor.spin()

    rotate_action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
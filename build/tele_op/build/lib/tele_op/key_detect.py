import tty
import sys
import termios
# ROS Client Library for Python
import rclpy
 
# Handles the creation of nodes
from rclpy.node import Node
 
# Enables usage of the String and Twist message type
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class KeyDetect(Node):
  """
  Create a MinimalPublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('keyboard_driver')
     
    # Create the publisher. This publisher will publish a String message
    # to the key_pressed topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(String, 'key_pressed', 10)
     
    # We will publish a message every 1 seconds
    timer_period = 1  # seconds
     
    # Create the timer
    self.timer = self.create_timer(timer_period, self.timer_callback)
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    print('Press w, x, a, d, and s for forward, backward, left, right and stop respectively')
  
  def timer_callback(self):
  	x= 0
  	x = sys.stdin.read(1)[0]
  	self.publisher_.publish(x)
  	self.get_logger().info('Publishing: "%s"' % x.data)

def main(args=None):
 
  # Initialize the rclpy library
  rclpy.init(args=args)
 
  # Create the node
  key_detect = KeyDetect()
 
  # Spin the node so the callback function is called.
  rclpy.spin(key_detect)
 
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  key_detect.destroy_node()
 
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
 
if __name__ == '__main__':
  main()



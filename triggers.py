"""
Example of how to use RC_CHANNEL_OVERRIDE messages to force input channels
in Ardupilot. These effectively replace the input channels (from joystick
or radio), NOT the output channels going to thrusters and servos.
"""

# Import mavutil
from pymavlink import mavutil
import time

import pygame
import time

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()
controller = pygame.joystick.Joystick(0)

# Get the name of the joystick and print it
print("Name of the joystick:")
print(controller.get_name())

# Get the number of axes
print("Number of axis:")
print(controller.get_numaxes())

# Create the connection
master = mavutil.mavlink_connection('udpin:0.0.0.0:14551')
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Create a function to send RC values
# More information about Joystick channels
# here: https://www.ardusub.com/operators-manual/rc-input-and-output.html#rc-inputs
def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.

print("setting rc channels")

while True:
    # Print the values for the axes
    pygame.event.pump()

    left_trigger = int(400*((controller.get_axis(4) / 2) + 0.5) + 1300)
    right_trigger = int(400*((controller.get_axis(5) / 2) + 0.5) + 1300)

    set_rc_channel_pwm(12, left_trigger)
    set_rc_channel_pwm(13, right_trigger)
    time.sleep(0.01)
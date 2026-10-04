import motor
from hub import port, motion_sensor, light_matrix, sound
import runloop
import math
import time

# Motor ports
left_motor = port.F
right_motor = port.E

# Wheel size constant
WHEEL_CIRCUMFERENCE_CM = 17.6

# PID constants
KP_STRAIGHT = 3
KI_STRAIGHT = 0
KD_STRAIGHT = 2 # .6

# PID state
integral_staight = 0
last_error_straight = 0

# Small motor limits
MAX_SPEED = 660
MIN_SPEED = -660
START_TIME = time.ticks_ms()

def Log(*args, sep=' ', end='\n', file=None, flush=False):
    """
    Log function that prints the current timestamp and all arguments, matching the print signature.
    """
    t = (time.ticks_ms() - START_TIME)/1000
    print(t, *args, sep=sep, end=end)

#😭😏😑😘🤗😸😮‍💨🤕😩✌️🤨😣🤩🤐😪🙁😝🤯😝🙁

def drive_straight_pid(distance_cm, target_angle, speed_dps=300):
    global integral_staight, last_error_straight

    speed_dps = max(min(speed_dps, MAX_SPEED), MIN_SPEED)

    motor.reset_relative_position(left_motor, 0)
    motor.reset_relative_position(right_motor, 0)

    degrees_to_rotate = (distance_cm * 360) / WHEEL_CIRCUMFERENCE_CM

    while True:
        yaw = motion_sensor.tilt_angles()[0]
        error = target_angle - yaw
        integral_staight += error
        derivative = error - last_error_straight
        correction = KP_STRAIGHT * error + KI_STRAIGHT * integral_staight + KD_STRAIGHT * derivative

        left_speed = speed_dps + correction
        right_speed = speed_dps - correction

        left_speed = max(min(left_speed, MAX_SPEED), MIN_SPEED)
        right_speed = max(min(right_speed, MAX_SPEED), MIN_SPEED)

        # Invert one motor's direction
        motor.run(left_motor, int(left_speed), acceleration=1000)
        motor.run(right_motor, int(-right_speed), acceleration=1000)
        # print("Degrees_to_rotate:", degrees_to_rotate,"Motor_relative_position:", motor.relative_position(left_motor), "Correction:", correction, "L:", left_speed, "R:", right_speed)
        last_error_straight = error
        time.sleep(0.01)

        avg_position = (abs(motor.relative_position(left_motor)) + abs(motor.relative_position(right_motor))) / 2
        if (avg_position) >= degrees_to_rotate:
            break
    motor.stop(left_motor)
    motor.stop(right_motor)

# PID constants and state
KP_TURN = .5
KI_TURN = 0
KD_TURN = 0
integral_turn = 0
last_error_turn = 0

#😭😏😑😘🤗😸😮‍💨🤕😩✌️🤨😣🤩🤐😪🙁😝🤯😝🙁

def turn(target_angle_deg, speed_dps=300, pivot_side=None, threshold=1.0):
    """
    Rotate in place to target_angle_deg using yaw PID.
    Prints current yaw to the console each loop for live graphing.
    """
    global integral_turn , last_error_turn

    # Clamp base speed
    speed_dps = max(min(speed_dps, MAX_SPEED), MIN_SPEED)

    # Reset gyro and PID state

    integral_turn = 0
    last_error_turn = 0

    while True:
        # Read yaw in degrees (–180…+180 or 0…360, depending on firmware)
        yaw = motion_sensor.tilt_angles()[0]

        # Print for SPIKE app’s live graph
        # print(yaw)

        # PID calculations
        error    = target_angle_deg - yaw
        integral_turn += error
        derivative = error - last_error_turn
        correction = KP_TURN*error + KI_TURN*integral_turn+ KD_TURN*derivative
        last_error_turn = error

        # Use correction as the speed for both motors, in opposite directions
        correction = max(min(correction, MAX_SPEED), MIN_SPEED)
        if pivot_side == 'left':
            # Left wheel stationary, right wheel moves
            motor.run(left_motor, 0, acceleration=1000)
            motor.run(right_motor, int(correction), acceleration=1000)
        elif pivot_side == 'right':
            # Right wheel stationary, left wheel moves
            motor.run(left_motor, int(correction), acceleration=1000)
            motor.run(right_motor, 0, acceleration=1000)
        else:
            # Both wheels move (default behavior)
            motor.run(left_motor, int(correction), acceleration=1000)
            motor.run(right_motor, int(correction), acceleration=1000)

        # Stop when within threshold
        if abs(error) <= threshold:
            break

        time.sleep(0.01)

    motor.stop(left_motor)
    motor.stop(right_motor)

#😭😏😑😘🤗😸😮‍💨🤕😩✌️🤨😣🤩🤐😪🙁😝🤯😝🙁

def initialize():
    motion_sensor.reset_yaw(0)
    drive_straight_pid(5, 0, speed_dps=-300)
    time.sleep (0.1)
    motion_sensor.reset_yaw(0)

#🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓🐓
async def main():

    # Heavy Lifting
    initialize()
    drive_straight_pid(66.75, 0, speed_dps=300)
    turn(-455, speed_dps= -300)
    drive_straight_pid(6, -450, speed_dps=300)
    await motor.run_for_degrees(port.A, 175, -30)
    drive_straight_pid(4, -450, speed_dps=300)
    Log("Heavy Lifting done")

    # Rectract arm
    await motor.run_for_degrees(port.A, 100, 30)
    retract_inprogress = motor.run_for_degrees(port.A, 75, 30)
    drive_straight_pid(10, -450, speed_dps=-300)
    await retract_inprogress
    drive_straight_pid(1.25, -450, speed_dps=300)
    Log("Heavy Lifting arm retracted")

    # Forge
    turn(450, speed_dps= 300)
    Log("Forge done")

    # Who lived here?
    drive_straight_pid(4, 450, speed_dps=300)

    # Get robot out of the corner
    turn(950, speed_dps= 300)
    turn(450, speed_dps= -300)
    drive_straight_pid(4, 450, speed_dps=-300)

    # Navigate behind what's on sale?
    turn(800, speed_dps= 300)
    drive_straight_pid(34, 800, speed_dps= 300)

    # Solve what's on sale?
    turn(460, speed_dps= 300)
    drive_straight_pid(20, 460, speed_dps= -300)
    time.sleep(0.1)
    Log("What's On Sale done")

    # Solve tip the scales
    drive_straight_pid(7, 450, speed_dps= 300)
    turn(-450, speed_dps= 300)
    await motor.run_for_degrees(port.B, 200, -100)
    await motor.run_for_degrees(port.B, 200, 100)
    Log("Tip the Scales done")

    # Navigate to blue base
    turn(750, speed_dps= 500)
    drive_straight_pid(20, 750, speed_dps= -600)
    turn(0, speed_dps= 500)
    drive_straight_pid(65, 0, speed_dps= -700)
    Log("Back home")


runloop.run(main())
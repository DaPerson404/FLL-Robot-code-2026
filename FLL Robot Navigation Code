import motor
from hub import port, motion_sensor, light_matrix, sound
import runloop
import time

LEFT_MOTOR_PORT = port.A
RIGHT_MOTOR_PORT = port.E
WHEEL_CIRCUMFERENCE_CM = 27.6


def drive_straight(distance_in_cm:int, degrees_per_second:int, direction:int):
    distance_moved=0
    motor.reset_relative_position(LEFT_MOTOR_PORT, 0)
    motor.reset_relative_position(RIGHT_MOTOR_PORT, 0)
    
    while distance_moved < distance_in_cm:
        motor.run(LEFT_MOTOR_PORT, int(-degrees_per_second), acceleration=1000)
        motor.run(RIGHT_MOTOR_PORT, int(degrees_per_second), acceleration=1000)
        distance_moved = (motor.relative_position(RIGHT_MOTOR_PORT) / 360) * WHEEL_CIRCUMFERENCE_CM
        print('distance moved ' + str(distance_moved))
    
    motor.stop(LEFT_MOTOR_PORT)
    motor.stop(RIGHT_MOTOR_PORT)


def drive_straight2(distance_in_cm:int, degrees_per_second:int, direction):
    if direction 
    distance_moved=0
    motor.reset_relative_position(LEFT_MOTOR_PORT, 0)
    motor.reset_relative_position(RIGHT_MOTOR_PORT, 0)
    while distance_moved < distance_in_cm:
        motor.run(LEFT_MOTOR_PORT, int(-degrees_per_second), acceleration=1000)
        motor.run(RIGHT_MOTOR_PORT, int(degrees_per_second), acceleration=1000)
        distance_moved = (motor.relative_position(RIGHT_MOTOR_PORT) / 360) * WHEEL_CIRCUMFERENCE_CM
        print('distance moved ' + str(distance_moved))
    motor.stop(LEFT_MOTOR_PORT)
    motor.stop(RIGHT_MOTOR_PORT)



def turn_to_degrees(direction: int, target_degrees:int):
        motion_sensor.reset_yaw(0)
        if target_degrees <= 30:
            degrees_per_second:int = 50
        elif target_degrees <= 90:
            degrees_per_second:int = 100
        else:
            degrees_per_second:int = 150
        target_decidegrees = 10 * target_degrees
        if target_degrees < 0:
            raise Exception("target_degrees has to be greater than or equal to zero. Got:" + str(target_degrees))
        remaining = target_degrees
        if direction == motor.CLOCKWISE:
            sign = 1
        else:
            sign = -1
        decidegrees_turned = 0
        while abs(decidegrees_turned) < target_decidegrees:
            speed = degrees_per_second
            print('remaining ' + str(remaining) + ' target_degrees ' + str(target_degrees))
            if remaining <= 30:
                speed = 50
            motor.run(LEFT_MOTOR_PORT, (sign * -speed), acceleration=1000)
            motor.run(RIGHT_MOTOR_PORT, (sign * -speed), acceleration=1000)
            yaw = motion_sensor.tilt_angles()[0]
            decidegrees_turned = abs(yaw)
            remaining = target_decidegrees - decidegrees_turned
            print('degrees turned = ' + str(decidegrees_turned) + " speed = " + str(speed))
        print ('yaw angle is ' + str(motion_sensor.tilt_angles()[0]))
        motor.stop(LEFT_MOTOR_PORT)
        print ('yaw angle is ' + str(motion_sensor.tilt_angles()[0]))
        motor.stop(RIGHT_MOTOR_PORT)
        print ('yaw angle is ' + str(motion_sensor.tilt_angles()[0]))
async def main():
    # write your code here
    drive_straight(80, 500)
    drive_straight(-80, 500)
    #drive_straight(30, 500)

runloop.run(main())

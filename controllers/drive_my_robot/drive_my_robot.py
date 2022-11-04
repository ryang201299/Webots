from controller import Robot

TIMESTEP = 64
MAX_SPEED = 6.1  # 6.28 // also referred to as angular velocity
NUM_SIDE = 4
LENGTH_SIDE = 0.25
WHEEL_RADIUS = 0.025
DISTANCE_BETWEEN_WHEELS = 0.09
DEGREES_IN_RADIANS = 6.28 # 360 degrees in radians

def initialise_robot():
    # Initialise robot object
    robot = Robot()

    # Create motor initialisations
    left_motor = robot.getDevice('motor_1')
    right_motor = robot.getDevice('motor_2')
    
    # Set default motor params
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    return left_motor, right_motor, robot
    
def initialise_environment(robot):
    start_time = robot.getTime()
    
    # Define environment for manuevering square
    # Vars for straight line
    linear_velocity = WHEEL_RADIUS * MAX_SPEED # actual speed
    duration_side = LENGTH_SIDE / linear_velocity
    
    # Vars for cornering
    angle_of_rotation = DEGREES_IN_RADIANS / NUM_SIDE
    rate_of_rotation = (2 * linear_velocity) / DISTANCE_BETWEEN_WHEELS
    duration_turn = angle_of_rotation / rate_of_rotation
    rot_start_time = start_time + duration_side
    rot_end_time = rot_start_time + duration_turn
    
    return duration_turn, rot_start_time, rot_end_time, duration_side
    
def run_time(tools, env_vars):
    # Separate robot motors from robot
    left_motor = tools[0]
    right_motor = tools[1]
    robot = tools[2]
    
    # Environment vars needed for motion
    duration_turn = env_vars[0]
    rot_start_time = env_vars[1]
    rot_end_time = env_vars[2]
    duration_side = env_vars[3]

    while robot.step(TIMESTEP) != -1:
        current_time = robot.getTime()
        
        # Set constant speed forward
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED
        
        # Begin rotation at end of side
        if rot_start_time < current_time < rot_end_time:
            left_speed = - MAX_SPEED
            right_speed = MAX_SPEED
         
        # End rotation at end of corner
        elif current_time > rot_end_time:
            rot_start_time = current_time + duration_side
            rot_end_time = rot_start_time + duration_turn    
                    
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
    
def main():
    # Initialise robot
    # Tools contains our robot, and left and right motors
    tools = initialise_robot()
    robot = tools[2]
   
    # Initialise environment
    # env_vars contains basic environment measurements like
    # length of sides, determined speed, rotation angles etc.
    env_vars = initialise_environment(robot)
    
    # Run environment
    run_time(tools, env_vars)
    
if __name__ == "__main__":
    main()
    
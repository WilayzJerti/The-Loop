# Basic Pomodoro timer with a 60-minute limit

import time

start_t = input('Set the timer (from 1 to 60 min):')
start_t = float(start_t)

# Check that the timer is greater than 0 and does not exceed 60 
if start_t > 0 and start_t <= 60:
    print(f'Timer set to:{int(start_t)} min')

    start_t = (start_t) * 60 # Convert minutes to seconds

    time.sleep(start_t)

    print('Timer expired')

elif start_t <= 0:
    print('Error: You tried to set the timer to 0 minutes or less.')
elif start_t > 60:
    print('Error: You tried to set the timer for more than 60 minutes.')
else:
    print('Error: Unknown error')

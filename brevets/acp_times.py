"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

MIN_SPEED = {
        0   : 15,
        600 : 11.428,
        1000: 13.333
        }

MAX_SPEED = {
        0   : 34,
        200 : 32,
        400 : 30,
        600 : 28,
        1000: 26
        }

DISTANCE_SPEED = {
    (0,200)    : 34,
    (200,400)  : 32,
    (400,600)  : 30,
    (600,1000) : 28,
    (1000,1200): 26
}


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # Error catching control longer than total race distance
    if control_dist_km > (brevet_dist_km * 1.2):
        control_dist_km = brevet_dist_km
    # Error catching if control distance is 0 or less, start time is the race start
    if control_dist_km <= 0:
        return brevet_start_time

    if control_dist_km <= (brevet_dist_km * 1.2):
        opening_times = []
        control_dist = control_dist_km
        for distance in DISTANCE_SPEED:
            dist = distance[1]-distance[0]
            if control_dist >= dist:
                time = ((dist / DISTANCE_SPEED[distance]) * 60)
                control_dist -=  dist
            else:
                time = ((control_dist / DISTANCE_SPEED[distance]) * 60)
                control_dist = 0

            opening_times.append(time)

    ride_time = sum(opening_times)
    ride_hours = math.floor(ride_time / 60)
    print(f'openH: {ride_hours}, dist:{control_dist_km}')
    ride_minutes = round(ride_time % 60)
    print(f'openM: {ride_minutes}, dist:{control_dist_km}')
    s_time = brevet_start_time.shift(hours=ride_hours, minutes=ride_minutes)
    return s_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    # Error catching if control distance is 0 or less, start time is the race start + 1 hour
    if control_dist_km <= 0:
        return brevet_start_time.shift(hours=1)

    # Calculate control closing time for distances form 0 to 600km
    if (control_dist_km <= 600) and (control_dist_km <= (brevet_dist_km * 1.2)):
        # Calculate control closing time for distances to 200km
        # By the rules, the overall time limit for a 200km brevet is 13H30
        if control_dist_km <= 200 and brevet_dist_km == 200:
            if control_dist_km == 200 or control_dist_km < 100:
                ride_time = (((control_dist_km / MIN_SPEED[0]) * 60) + 10)
            else:
                ride_time = ((control_dist_km / MIN_SPEED[0]) * 60)
        else:
            ride_time = ((control_dist_km / MIN_SPEED[0]) * 60)

    # Calculate control closing time for distances between 600km and 1200km
    if (control_dist_km > 600) and (control_dist_km <= (brevet_dist_km * 1.2)):
        ride_time = ((600 / MIN_SPEED[0]) * 60)
        ride_time += (((control_dist_km-600)/MIN_SPEED[600])*60)

    ride_hours = math.floor((ride_time / 60))
    #print(f'closeH= {ride_hours}, dist:{control_dist_km}')
    ride_minutes = round((ride_time % 60))
    #print(f'closeM= {ride_minutes}, dist:{control_dist_km}')
    c_time = brevet_start_time.shift(hours=ride_hours, minutes=ride_minutes)

    return c_time

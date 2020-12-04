#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import copy
import sys
sys.path.insert(1, '/home/wencen/Documents/cmpe295/simulation')
import config as config
import math 

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")
cf.All_Green_Light(sim)

spawns = sim.get_spawn()
forward = lgsvl.utils.transform_to_forward(spawns[0])

# Weather variable
time_of_day = [12.00]
weather = [[0.0, 0.0, 0.0]]   #[rain, fog, wetness]

# Ego Car Variable
ego_speed = 6

def turn():
   
    waypoints = []
    x_max = 2
    z_delta = 12

    layer_mask = 0
    layer_mask |= 1 << 0 # 0 is the layer for the road (default)

    for i in range(20):
        speed = 24# if i % 2 == 0 else 12
        px = 0
        pz = (i + 1) * z_delta
        # Waypoint angles are input as Euler angles (roll, pitch, yaw)
        angle = spawns[0].rotation
        # Raycast the points onto the ground because BorregasAve is not flat
        hit = sim.raycast(spawns[0].position + pz * forward, lgsvl.Vector(0,-1,0), layer_mask) 

        # NPC will wait for 1 second at each waypoint
        wp = lgsvl.DriveWaypoint(hit.point, speed, angle, 1)
        waypoints.append(wp)

    # When the NPC is within 0.5m of the waypoint, this will be called
    def on_waypoint(agent, index):
        print("waypoint {} reached".format(index))

    # The above function needs to be added to the list of callbacks for the NPC
    ego.on_waypoint_reached(on_waypoint)

    # The NPC needs to be given the list of waypoints. 
    # A bool can be passed as the 2nd argument that controls whether or not the NPC loops over the waypoints (default false)
    ego.follow(waypoints)
    


for time in time_of_day:
  for weatherInfo in weather:

    # ego vehicle
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.velocity = ego_speed * forward
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
    print("ego spawn", state.transform)

    turn()

    #set time of day
    sim.set_time_of_day(time)

    #set weather of day  ## rainy day
    sim.weather = lgsvl.WeatherState(rain=weatherInfo[0], fog=weatherInfo[1], wetness=weatherInfo[2])


    vehicles = {
      ego: "EGO",
    }

    input("Press Enter to run next scenario")
    print("The time is {} ".format(time_of_day))
    print("The weather condition is rain={}, fog={}, wetness={}".format(weatherInfo[0],weatherInfo[1],weatherInfo[2]))
    sim.run(time_limit = 8.0)
    sim.reset()



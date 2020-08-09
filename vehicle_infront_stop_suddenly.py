#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import simulation.config as config
import copy

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")
cf.All_Green_Light(sim)

spawns = sim.get_spawn()

# Weather variable
time_of_day = [12.00, 18.00, 24.00]
weather = [[0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]   #[rain, fog, wetness]

#Variable on the road compare to spawns[0]
# [forward, right]
ego_position = [0, 0]
npc_position = [20, 0]
ego_speed = 10
npc_speed = 12

forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# When the NPC is within 0.5m of the waypoint, this will be called
def on_waypoint(agent, index):
  print("waypoint {} reached".format(index))
  print("npc vehicle stop")

def on_collision(agent1, agent2, contact):
  name1 = vehicles[agent1]
  name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
  print("{} collided with {}".format(name1, name2))

for time in time_of_day:
  for weatherInfo in weather:

    #set time of day
    sim.set_time_of_day(time)

    #set weather of day  ## rainy day
    sim.weather = lgsvl.WeatherState(rain=weatherInfo[0], fog=weatherInfo[1], wetness=weatherInfo[2])

    # EGO
    state = copy.deepcopy(lgsvl.AgentState())
    state.velocity = ego_speed * forward
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position +  + ego_position[0] * forward
    a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    #NPC sedan
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + npc_position[0] * forward
    state.transform.rotation = spawns[0].rotation
    npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

    vehicles = {
      a: "EGO",
      npc: "Sedan",
    }

    a.on_collision(on_collision)
    npc.on_collision(on_collision)

    waypoints = []
    z_delta = 30

    layer_mask = 0
    layer_mask |= 1 << 0 # 0 is the layer for the road (default)

    # Waypoint angles are input as Euler angles (roll, pitch, yaw)
    angle = spawns[0].rotation
    hit = sim.raycast(spawns[0].position + (2*z_delta + npc_position[0]) * forward, lgsvl.Vector(0,-1,0), layer_mask) 

    # NPC will wait for 1 second at each waypoint
    wp = lgsvl.DriveWaypoint(hit.point, npc_speed, angle, 1)
    waypoints.append(wp)

    # The above function needs to be added to the list of callbacks for the NPC
    npc.on_waypoint_reached(on_waypoint)
    npc.follow(waypoints)

    input("Press Enter to run next scenario")
    print("The time is {} ".format(time_of_day))
    print("The weather condition is rain={}, fog={}, wetness={}".format(weatherInfo[0],weatherInfo[1],weatherInfo[2]))
    sim.run(time_limit = 10.0)
    sim.reset()

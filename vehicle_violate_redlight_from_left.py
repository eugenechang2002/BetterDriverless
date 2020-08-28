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

#variable
ego_position = [10, 0]
npc_position = [40, -30]
ego_speed = 4
npc_speed = 6

for time in time_of_day:
  for weatherInfo in weather:
    #set time of day
    sim.set_time_of_day(time)

    #set weather of day  ## rainy day
    sim.weather = lgsvl.WeatherState(rain=weatherInfo[0], fog=weatherInfo[1], wetness=weatherInfo[2])

    forward = lgsvl.utils.transform_to_forward(spawns[0])
    right = lgsvl.utils.transform_to_right(spawns[0])

    #ego vehicle
    state = copy.deepcopy(lgsvl.AgentState())
    state.velocity = ego_speed * forward
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + ego_position[0]*forward
    a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    #npc vehicle
    state = copy.deepcopy(lgsvl.AgentState())
    state.velocity = npc_speed * right
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + npc_position[0]*forward + npc_position[1]*right
    state.transform.rotation.y = spawns[0].rotation.y + 90.0
    vehicle_at_right_intersection = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

    # The bounding box of an agent are 2 points (min and max) such that the box formed from those 2 points completely encases the agent
    input("Press Enter to run next scenario")
    print("The time is {} ".format(time_of_day))
    print("The weather condition is rain={}, fog={}, wetness={}".format(weatherInfo[0],weatherInfo[1],weatherInfo[2]))
    sim.run(time_limit = 8.0)
    sim.reset()

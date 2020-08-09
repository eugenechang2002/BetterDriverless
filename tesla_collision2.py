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

forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# Weather variable
time_of_day = [12.00, 18.00, 24.00]
weather = [[0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]   #[rain, fog, wetness]

# Ego Car Variable
ego_speed = 6

def on_collision(agent1, agent2, contact):
  name1 = vehicles[agent1]
  print("{} collided with at {}".format(name1, contact))

for time in time_of_day:
  for weatherInfo in weather:

    # ego vehicle
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.velocity = ego_speed * forward
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)


    # school bus, 20m ahead, perpendicular to road, stopped
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + 40.0 * forward
    state.transform.rotation.y = spawns[0].rotation.y + 270.0
    state.transform.rotation.x = spawns[0].rotation.x + 90.0   #bus rotate then fall
    bus = sim.add_agent("SchoolBus", lgsvl.AgentType.NPC, state)

    #set time of day
    sim.set_time_of_day(time)

    #set weather of day  ## rainy day
    sim.weather = lgsvl.WeatherState(rain=weatherInfo[0], fog=weatherInfo[1], wetness=weatherInfo[2])


    vehicles = {
      ego: "EGO",
      bus: "SchoolBus",
    }

    # The above on_collision function needs to be added to the callback list of each vehicle
    ego.on_collision(on_collision)
    bus.on_collision(on_collision)

    input("Press Enter to run next scenario")
    print("The time is {} ".format(time_of_day))
    print("The weather condition is rain={}, fog={}, wetness={}".format(weatherInfo[0],weatherInfo[1],weatherInfo[2]))
    sim.run(time_limit = 12.0)
    sim.reset()

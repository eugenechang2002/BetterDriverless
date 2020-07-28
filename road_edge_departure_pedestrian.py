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

#variable
time_of_day = [12.00, 18.00, 24.00]
weather = [[0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]   #[rain, fog, wetness]

#variables
ego_position = [150, 30]  #the forward, right position for parking spot
pedestrian_spot = [140, 5]  #the forward, right position for npcSpot spot
pedestrian_speed = 1    #npcSpeed in terms of forward
ego_speed = 3


for time in time_of_day:
  for weatherInfo in weather:

    #npc ##add pedestrian
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.velocity = pedestrian_speed * forward

    # Give waypoints for the spawn location and walk 10m ahead
    start = spawns[0].position + pedestrian_spot[0]*forward + pedestrian_spot[1]*right
    end =  start + 10 * forward
    wp = [ lgsvl.WalkWaypoint(start, 0),
           lgsvl.WalkWaypoint(end, 0),
         ]

    state.transform.position = start
    state.transform.rotation = spawns[0].rotation
    pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, state)
    pedestrian.follow(wp, True)

    #ego
    state = copy.deepcopy(lgsvl.AgentState())
    state.velocity = ego_speed * right *  -1
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + ego_position[0]*forward + ego_position[1]*right
    state.transform.rotation.y = spawns[0].rotation.y + 270.0
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    #set time of day
    sim.set_time_of_day(time)

    #set weather of day  ## rainy day
    sim.weather = lgsvl.WeatherState(rain=weatherInfo[0], fog=weatherInfo[1], wetness=weatherInfo[2])

    vehicles = {
      ego: "EGO",
      pedestrian: "Bob",
    }

    def on_collision(agent1, agent2, contact):
      name1 = vehicles[agent1]
      print("{} collided with at {}".format(name1, contact))

    # The above on_collision function needs to be added to the callback list of each vehicle
    ego.on_collision(on_collision)
    pedestrian.on_collision(on_collision)

    input("Press Enter to run next scenario")
    print("The time is {} ".format(time_of_day))
    print("The weather condition is rain={}, fog={}, wetness={}".format(weatherInfo[0],weatherInfo[1],weatherInfo[2]))
    sim.run(time_limit = 11.0)
    sim.reset()


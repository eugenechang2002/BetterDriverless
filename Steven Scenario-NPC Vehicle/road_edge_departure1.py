#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import copy

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
if sim.current_scene == "BorregasAve":
  sim.reset()
else:
  sim.load("BorregasAve")

spawns = sim.get_spawn()
npcState = spawns[0];

sx = spawns[0].position.x
sz = spawns[0].position.z
ry = spawns[0].rotation.y

forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

#variables
parkingSpot = [150, 10]  #the forward, right position for parking spot
npcSpot = [130, 0]  #the forward, right position for npcSpot spot
npcSpeed = 4    #npcSpeed in terms of forward
egoSpeed = 2
time_of_day = 24.00

#npc
state = lgsvl.AgentState()
state.velocity = npcSpeed * forward 
state.transform = spawns[0]
state.transform.position = spawns[0].position + npcSpot[0]*forward + npcSpot[1]*right
state2 = copy.deepcopy(state)
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state2)

#ego
state = lgsvl.AgentState()
state.velocity = egoSpeed * right *  -1
state.transform.position = spawns[0].position + (parkingSpot[0]-npcSpot[0])*forward + (parkingSpot[1]-npcSpot[1])*right
state.transform.rotation.y = spawns[0].rotation.y + 270.0
ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

#set time of day
sim.set_time_of_day(time_of_day)

#set weather of day
sim.weather = lgsvl.WeatherState(rain=0.5, fog=0.0, wetness=0.5)

vehicles = {
  ego: "EGO",
  npc: "Sedan",
}

def on_collision(agent1, agent2, contact):
  name1 = vehicles[agent1]
  print("{} collided with at {}".format(name1, contact))

# The above on_collision function needs to be added to the callback list of each vehicle
ego.on_collision(on_collision)
npc.on_collision(on_collision)

input("Press Enter to run")

sim.run()

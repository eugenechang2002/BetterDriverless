#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import math

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
if sim.current_scene == "BorregasAve":
  sim.reset()
else:
  sim.load("BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]

forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

state.velocity = 6 * forward
state.transform.position = spawns[0].position + 10*forward
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

state = lgsvl.AgentState()
state.velocity = 5 * right * -1 
state.transform.position = spawns[0].position + 50.0 * forward + 30 * right
state.transform.rotation.y = spawns[0].rotation.y + 270.0
vehicle_at_right_intersection = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)



# The bounding box of an agent are 2 points (min and max) such that the box formed from those 2 points completely encases the agent
print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)
print("a npc vehicle would approach from the right")

sim.run()

#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import simulation.config as config
import lgsvl
import random
import time
import math

random.seed(0)

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")
spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])


for i, name in enumerate(["Sedan", "SUV", "Jeep", "Hatchback"]):
  state = lgsvl.AgentState()
  # 10 meters ahead
  state.transform.position = spawns[0].position + (10 * forward) - (4.0 * i * right)
  state.transform.rotation = spawns[0].rotation
  sim.add_agent(name, lgsvl.AgentType.NPC, state)

input("Press Enter to reset")

# Reset will remove any spawned vehicles and set the weather back to default, but will keep the scene loaded
sim.reset()
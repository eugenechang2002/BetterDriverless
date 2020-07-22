#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import simulation.config as config
import lgsvl

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

sensors = a.get_sensors()
for s in sensors:
  if s.name == "Lidar":
    s.save("lidar.pcd")
    break
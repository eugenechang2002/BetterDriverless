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

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

# An EGO will not connect to a bridge unless commanded to
print("Bridge connected:", a.bridge_connected)

# The EGO is now looking for a bridge at the specified IP and port
a.connect_bridge("127.0.0.1", 9090)

print("Waiting for connection...")

while not a.bridge_connected:
  time.sleep(1)

print("Bridge connected:", a.bridge_connected)

sensors = a.get_sensors()

# Sensors have an enabled/disabled state that can be set
# By default all sensors are enabled
# Disabling sensor will prevent it to send or receive messages to ROS or Cyber bridges
for s in sensors:
  print(type(s), s.enabled)

sim.run()
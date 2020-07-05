#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import simulation.config as config

cf = config.Config()
sim = cf.Simulator()

print("Current Scene = {}".format(sim.current_scene))

# Loads the named map in the connected simulator. The available maps can be set up in web interface
cf.LoadOrResetScene(sim, "BorregasAve")
print("Current Scene = {}".format(sim.current_scene))

# This will print out the position and rotation vectors for each of the spawn points in the loaded map
spawns = sim.get_spawn()
for spawn in sim.get_spawn():
  print(spawn)

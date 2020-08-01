#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import simulation.config as config
import lgsvl
import random
import copy

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")

spawns = sim.get_spawn()

sim.set_time_of_day(10, fixed=True)
print("Current time of day:", sim.time_of_day)

state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])


state = lgsvl.AgentState()
state.transform.position = spawns[0].position +(10 * forward)
state.transform.rotation.y = spawns[0].rotation.y
suv = sim.add_agent("SUV", lgsvl.AgentType.NPC, state)


state = lgsvl.AgentState()
state.transform.position = spawns[0].position + 3*right
state.transform.rotation.y = spawns[0].rotation.y
sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)



start = spawns[0].position + 25*forward
end =  start - 10*right
wp = [ lgsvl.WalkWaypoint(start, 0),
        lgsvl.WalkWaypoint(end, 0),
      ]


state.transform.position = start
state.transform.rotation = spawns[0].rotation
pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, state)
pedestrian.follow(wp, True)

cf.All_Green_Light(sim)
sedan.follow_closest_lane(True, 35)
sedan.follow_closest_lane(True, 35)
sedan.follow_closest_lane(True, 35)
suv.follow_closest_lane(True, 35)
suv.follow_closest_lane(True, 35)
suv.follow_closest_lane(True, 35)
sim.run(30)